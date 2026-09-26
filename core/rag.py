import json
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
embedding_texts = []

pasta_data = Path("data")
pasta_data.mkdir(exist_ok=True)


def format_item(item):
    """
    Converte um item de trade para texto legível.
    """
    name = item.get("name", "Unknown")
    category = item.get("category", "Unknown")
    quantity = item.get("quantity", 1)
    variant = item.get("variant")
    value = item.get("unit_value_raw", "N/A")
    demand = item.get("demand", "N/A")

    text = f"{quantity}x {name}"

    if variant:
        text += f" [{variant}]"

    text += (
        f" | Category: {category}"
        f" | Value: {value}"
        f" | Demand: {demand}/10"
    )

    return text


def format_trade(document):
    """
    Converte um trade_listing para uma representação textual
    mais clara para embedding e para o LLM.
    """
    offering = document.get("offering", {})
    requesting = document.get("requesting", {})

    lines = [
        "TRADE LISTING",
        f"Trader: {document.get('trader', 'Unknown')}",
        f"Posted: {document.get('posted_ago', 'Unknown')}",
        f"Source label: {document.get('site_label') or 'None'}",
        "",
        "TRADER OFFERS:"
    ]

    offering_items = offering.get("items", [])

    if offering_items:
        for item in offering_items:
            lines.append(f"- {format_item(item)}")
    else:
        lines.append("- No specific items")

    offering_directives = offering.get("directives", [])

    if offering_directives:
        lines.append(
            "Offer directives: "
            + ", ".join(offering_directives)
        )

    lines.extend([
        f"Offer total value: "
        f"{offering.get('display_total_value_raw', 'N/A')}",
        f"Offer average demand: "
        f"{offering.get('display_avg_demand', 'N/A')}",
        "",
        "TRADER WANTS IN RETURN:"
    ])

    requesting_items = requesting.get("items", [])

    if requesting_items:
        for item in requesting_items:
            lines.append(f"- {format_item(item)}")
    else:
        lines.append("- No specific items")

    requesting_directives = requesting.get("directives", [])

    if requesting_directives:
        lines.append(
            "Request directives: "
            + ", ".join(requesting_directives)
        )

    lines.extend([
        f"Requested total value: "
        f"{requesting.get('display_total_value_raw', 'N/A')}",
        f"Requested average demand: "
        f"{requesting.get('display_avg_demand', 'N/A')}",
    ])

    description = document.get("description")

    if description:
        lines.extend([
            "",
            f"Trader description: {description}"
        ])

    return "\n".join(lines)


def format_market_item(document):
    """
    Representação textual dos documentos da tabela de valores.
    """
    lines = [
        "MARKET ITEM",
        f"Name: {document.get('name', 'Unknown')}",
        f"Category: {document.get('category', 'Unknown')}",
    ]

    if document.get("rarity"):
        lines.append(
            f"Rarity: {document['rarity']}"
        )

    if document.get("variant"):
        lines.append(
            f"Variant: {document['variant']}"
        )

    lines.extend([
        f"Trading value: {document.get('value', 'N/A')}",
        f"Source status: {document.get('status', 'N/A')}",
        f"Demand: {document.get('demand', 'N/A')}",
    ])

    if document.get("beli_price"):
        lines.append(
            f"In-game Beli price: {document['beli_price']}"
        )

    if document.get("robux_price"):
        lines.append(
            f"Robux price: {document['robux_price']}"
        )

    if document.get("fruit_type"):
        lines.append(
            f"Fruit type: {document['fruit_type']}"
        )

    if document.get("updated"):
        lines.append(
            f"Source updated: {document['updated']}"
        )

    return "\n".join(lines)


def format_document(document):
    """
    Decide como representar cada tipo de documento.
    """
    if document.get("type") == "trade_listing":
        return format_trade(document)

    return format_market_item(document)


def document_signature(document):
    """
    Cria uma assinatura para impedir que anúncios praticamente
    idênticos dominem o top-k.
    """

    if document.get("type") != "trade_listing":
        return (
            "market",
            document.get("name"),
            document.get("category"),
            document.get("variant")
        )

    offering = document.get("offering", {})
    requesting = document.get("requesting", {})

    def item_signature(items):
        return tuple(
            sorted(
                (
                    item.get("name"),
                    item.get("variant"),
                    item.get("quantity", 1)
                )
                for item in items
            )
        )

    return (
        "trade",
        document.get("trader"),
        item_signature(offering.get("items", [])),
        item_signature(requesting.get("items", [])),
        tuple(sorted(offering.get("directives", []))),
        tuple(sorted(requesting.get("directives", [])))
    )


# =========================================================
# CARREGAMENTO
# =========================================================

for arquivo in pasta_data.rglob("*.jsonl"):
    try:
        with open(
            arquivo,
            "r",
            encoding="utf-8"
        ) as f:

            for linha in f:
                linha = linha.strip()

                if not linha:
                    continue

                try:
                    document = json.loads(linha)

                    # Metadata não entra no FAISS
                    if document.get("type") == "metadata":
                        continue

                    documents.append(document)

                    embedding_texts.append(
                        format_document(document)
                    )

                except json.JSONDecodeError:
                    print(
                        f"Linha JSON inválida em {arquivo}"
                    )

    except Exception as e:
        print(
            f"Erro ao ler {arquivo}: {e}"
        )


if not documents:
    raise ValueError(
        "Nenhum documento encontrado."
    )


# =========================================================
# EMBEDDINGS
# =========================================================

embeddings = model.encode(
    embedding_texts,
    convert_to_numpy=True
).astype("float32")


dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)


print(
    "Quantidade de documentos:",
    len(documents)
)

print(
    "Quantidade de vetores:",
    index.ntotal
)


# =========================================================
# RAG
# =========================================================

class RAG:

    @classmethod
    def search(cls, query, k=20):

        query_embedding = model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        # Buscamos mais candidatos porque alguns serão
        # descartados pela deduplicação.
        candidate_k = min(
            k * 4,
            len(documents)
        )

        distances, indices = index.search(
            query_embedding,
            candidate_k
        )

        results = []
        signatures = set()

        for i in indices[0]:

            if i == -1:
                continue

            document = documents[i]

            signature = document_signature(
                document
            )

            if signature in signatures:
                continue

            signatures.add(signature)

            results.append(
                format_document(document)
            )

            if len(results) >= k:
                break

        return results