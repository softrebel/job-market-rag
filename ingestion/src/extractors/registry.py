"""
Single place that knows which extractors exist. Adding a new source
means: write the extractor, register it here, add its name to
`enabled_sources` in config — nothing else in the pipeline changes.
"""

from config.settings import settings
from extractors.base import BaseExtractor
from extractors.postgres_extractor.extractor import PostgresExtractor
from extractors.crawlers.jobinja import JobinjaCrawler

_ALL_EXTRACTORS: dict[str, type[BaseExtractor]] = {
    "postgres_source": PostgresExtractor,
    "jobinja": JobinjaCrawler,
}


# def get_enabled_extractors() -> list[BaseExtractor]:
#     return [
#         _ALL_EXTRACTORS[name]()
#         for name in settings.ENABLED_SOURCES
#         if name in _ALL_EXTRACTORS
#     ]
