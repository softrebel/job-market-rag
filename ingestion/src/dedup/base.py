from abc import ABC, abstractmethod


class DedupStore(ABC):
    @abstractmethod
    def mark_if_new(
        self,
        key: str,
        ttl: int | None = None,
    ) -> bool:
        """
        Returns:
            True  -> key is new and marked
            False -> key already exists
        """
        pass

    # @abstractmethod
    # def add(self, key: str, ttl: int | None = None) -> None:
    #     pass
