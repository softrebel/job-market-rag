from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)


def test_embedding():

    embedder = SentenceTransformerEmbedder()

    texts = [
        "استخدام برنامه نویس Python",
        "Senior Backend Developer",
    ]

    vectors = embedder.embed(texts)

    assert len(vectors) == 2

    assert len(vectors[0]) > 0

    assert len(vectors[0]) == len(vectors[1])
