from extractors.base import BaseExtractor
from collections.abc import Iterator
from datetime import datetime
from domain.canonical_job import CanonicalJob
from repositories.job_repository import JobRepository
from config.logging import logger
from mappers.job_canonical_mapper import CanonicalJobMapper
from database.session import Job


class PostgresExtractor(BaseExtractor):
    source_name = "postgres_source"

    def __init__(self, repo: JobRepository):
        self.repo = repo

    def iter_raw_documents(
        self, since: datetime | None = None
    ) -> Iterator[CanonicalJob]:
        last_id = 0
        try:
            while True:
                rows: list[Job] | None = self.repo.fetch_jobs_batch(last_id=last_id)
                if not rows:
                    break
                for row in rows:
                    yield CanonicalJobMapper.job_to_canonical(row)
                    last_id = row.id
        except Exception as e:
            logger.error("Error on Iter Documents", e)
