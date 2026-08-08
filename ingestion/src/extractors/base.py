"""
Common contract every data source implements. Downstream code
(cleaning, chunking, Celery tasks) never needs to know whether a
RawDocument came from Postgres or a crawled site — it only depends
on this interface.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from datetime import datetime

from domain.canonical_job import CanonicalJob


class BaseExtractor(ABC):
    # Short, stable identifier stored on every RawDocument for
    # provenance/debugging (e.g. "postgres_source", "site_a").
    source_name: str

    @abstractmethod
    def iter_raw_documents(self, since: datetime | None = None) -> Iterator[CanonicalJob]:
        """
        Yield RawDocument objects. `since` lets an extractor do an
        incremental run (only new/updated content) when supported.
        """
        raise NotImplementedError
