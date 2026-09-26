import os
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Carrega o modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
pasta_data = Path("data")

# Garante que a pasta 'data' existe
pasta_data.mkdir(exist_ok=True)

# rglob("*.txt") busca todos os arquivos .txt na pasta e em qualquer subpasta
for arquivo in pasta_data.rglob("*.txt"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if conteudo:  # Ignora arquivos vazios
                documents.append(conteudo)
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}: {e}")

# Validação crítica caso nenhuma subpasta tenha arquivos válidos
if not documents:
    raise ValueError(
        "Nenhum arquivo .txt com conteúdo foi encontrado em 'data' ou em suas subpastas."
    )

# Gera os embeddings
embeddings = model.encode(documents, convert_to_numpy=True).astype("float32")

# Cria o índice FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("Quantidade de documentos:", len(documents))
print("Quantidade de vetores:", index.ntotal)


class RAG:
    @classmethod
    def search(cls, query, k=10):
        query_embedding = model.encode([query]).astype("float32")
        distances, indices = index.search(query_embedding, k)

        results = []
        for i in indices[0]:
            if i != -1 and i < len(documents):
                results.append(documents[i])

        return results