from sentence_transformers import SentenceTransformer

from app.embeddings.base import BaseEmbedder


class SentenceTransformerEmbedder(BaseEmbedder):
    def __init__(
        self,
        model_name: str,
    ):
        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        return self.model.get_embedding_dimension()
