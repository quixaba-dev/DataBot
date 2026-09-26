import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


class RAG:
    """
    Sistema genérico de Retrieval-Augmented Generation.

    Responsável por:
    - descobrir fontes de conhecimento;
    - extrair texto de formatos suportados;
    - dividir documentos em chunks;
    - gerar embeddings;
    - indexar os vetores com FAISS;
    - recuperar contexto semanticamente relevante.

    A ausência de fontes de conhecimento não é considerada um erro.
    """

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".md",
        ".json",
        ".jsonl",
    }

    def __init__(
        self,
        data_dir="data",
        model_name="all-MiniLM-L6-v2",
        chunk_size=1000,
        chunk_overlap=150,
    ):
        self.data_dir = Path(data_dir)

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.documents = []
        self.index = None

        self.data_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.model = SentenceTransformer(
            model_name
        )

        self._load_documents()

        if self.documents:
            self._build_index()

    # =========================================================
    # STATE
    # =========================================================

    @property
    def available(self):
        """
        Indica se existe uma base de conhecimento carregada
        e pronta para busca.
        """
        return (
            self.index is not None
            and len(self.documents) > 0
        )

    # =========================================================
    # DOCUMENT LOADING
    # =========================================================

    def _load_documents(self):
        """
        Procura recursivamente arquivos suportados dentro
        do diretório de conhecimento.
        """

        for path in self.data_dir.rglob("*"):

            if not path.is_file():
                continue

            if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            try:
                documents = self._read_file(path)

                for document in documents:

                    if not isinstance(document, str):
                        continue

                    document = document.strip()

                    if not document:
                        continue

                    self.documents.extend(
                        self._chunk_text(document)
                    )

            except Exception as e:
                print(
                    f"Erro ao carregar {path}: {e}"
                )

    def _read_file(self, path):
        """
        Seleciona o parser apropriado para cada extensão.
        """

        extension = path.suffix.lower()

        if extension in {".txt", ".md"}:
            return self._read_text(path)

        if extension == ".json":
            return self._read_json(path)

        if extension == ".jsonl":
            return self._read_jsonl(path)

        return []

    # =========================================================
    # TEXT / MARKDOWN
    # =========================================================

    def _read_text(self, path):
        """
        Carrega arquivos de texto simples ou Markdown.
        """

        content = path.read_text(
            encoding="utf-8"
        )

        return [content]

    # =========================================================
    # JSON
    # =========================================================

    def _read_json(self, path):
        """
        Carrega um documento JSON.

        Objetos e arrays são convertidos para uma
        representação textual genérica.
        """

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):

            return [
                self._json_to_text(item)
                for item in data
            ]

        return [
            self._json_to_text(data)
        ]

    # =========================================================
    # JSONL
    # =========================================================

    def _read_jsonl(self, path):
        """
        Carrega arquivos JSON Lines.

        Cada linha válida é considerada um documento
        independente.
        """

        documents = []

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            for line_number, line in enumerate(
                file,
                start=1
            ):

                line = line.strip()

                if not line:
                    continue

                try:
                    data = json.loads(line)

                    documents.append(
                        self._json_to_text(data)
                    )

                except json.JSONDecodeError:

                    print(
                        f"JSON inválido em {path} "
                        f"(linha {line_number})"
                    )

        return documents

    def _json_to_text(self, data):
        """
        Converte qualquer estrutura JSON em texto
        sem assumir um schema específico.
        """

        if isinstance(data, str):
            return data

        return json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )

    # =========================================================
    # CHUNKING
    # =========================================================

    def _chunk_text(self, text):
        """
        Divide documentos grandes em chunks com overlap
        para reduzir perda de contexto entre divisões.
        """

        text = text.strip()

        if not text:
            return []

        if len(text) <= self.chunk_size:
            return [text]

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start = end - self.chunk_overlap

        return chunks

    # =========================================================
    # EMBEDDINGS / FAISS
    # =========================================================

    def _build_index(self):
        """
        Gera embeddings para todos os documentos e constrói
        o índice vetorial FAISS.
        """

        embeddings = self.model.encode(
            self.documents,
            convert_to_numpy=True
        ).astype("float32")

        # Normalização permite utilizar similaridade
        # por produto interno como cosine similarity.
        faiss.normalize_L2(
            embeddings
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(
            embeddings
        )

        print(
            "Quantidade de documentos:",
            len(self.documents)
        )

        print(
            "Quantidade de vetores:",
            self.index.ntotal
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def search(
        self,
        query,
        k=15,
        min_score=None
    ):
        """
        Recupera os documentos semanticamente mais próximos
        da consulta.

        Caso nenhuma base de conhecimento esteja disponível,
        retorna uma lista vazia.

        min_score pode ser utilizado para descartar resultados
        com baixa similaridade.
        """

        if not self.available:
            return []

        if not query or not query.strip():
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(
            query_embedding
        )

        candidate_k = min(
            k,
            len(self.documents)
        )

        scores, indices = self.index.search(
            query_embedding,
            candidate_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            if (
                min_score is not None
                and score < min_score
            ):
                continue

            results.append(
                self.documents[index]
            )

        return results