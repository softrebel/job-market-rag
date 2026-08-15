from app.config.settings import settings
from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)


def main():

    print(f"Loading model: {settings.embedding_model}")

    embedder = SentenceTransformerEmbedder(settings.embedding_model)

    query = "استخدام برنامه نویس ارشد پایتون در تهران"

    vector = embedder.embed_query(query)

    print(f"Model: {settings.embedding_model}")

    print(f"Dimension: {embedder.dimension}")

    print(f"Vector length: {len(vector)}")

    print(f"First 10 values: {vector[:10]}")


if __name__ == "__main__":
    main()
