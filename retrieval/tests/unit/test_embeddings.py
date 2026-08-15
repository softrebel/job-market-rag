from app.embeddings.base import BaseEmbedder


class FakeEmbedder(BaseEmbedder):
    def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return [[1.0, 2.0, 3.0] for _ in texts]

    @property
    def dimension(self) -> int:
        return 3


def test_embed_query():

    embedder = FakeEmbedder()

    vector = embedder.embed_query("Python developer")

    assert vector == [1.0, 2.0, 3.0]


def test_embed_multiple_texts():

    embedder = FakeEmbedder()

    vectors = embedder.embed(
        [
            "Python developer",
            "Backend developer",
        ]
    )

    assert len(vectors) == 2
    assert len(vectors[0]) == 3


def test_dimension():

    embedder = FakeEmbedder()

    assert embedder.dimension == 3
