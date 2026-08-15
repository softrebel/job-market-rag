from abc import ABC, abstractmethod


class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        pass

    def embed_query(self, query: str) -> list[float]:
        vectors = self.embed([query])

        if not vectors:
            raise ValueError("Embedding model returned no vector.")

        return vectors[0]

    @property
    @abstractmethod
    def dimension(self) -> int:
        pass
