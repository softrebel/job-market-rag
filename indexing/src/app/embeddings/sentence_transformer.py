from sentence_transformers import SentenceTransformer

from app.config.settings import settings
from app.embeddings.base import BaseEmbedder


class SentenceTransformerEmbedder(BaseEmbedder):
    def __init__(
        self,
        model_name: str | None = None,
        device: str | None = None,
    ):
        self.model_name = model_name or settings.EMBEDDING_MODEL

        self.device = device or settings.EMBEDDING_DEVICE

        self.model = SentenceTransformer(
            self.model_name,
            device=self.device,
        )

    @property
    def dimension(self) -> int:
        return self.model.get_embedding_dimension()

    def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            batch_size=settings.EMBEDDING_BATCH_SIZE,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()
