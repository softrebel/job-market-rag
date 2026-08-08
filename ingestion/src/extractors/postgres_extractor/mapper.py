from domain.job import Job
from domain.canonical_job import CanonicalJob


class CanonicalJobMapper:
    @staticmethod
    def canonical_to_job(canonical: CanonicalJob) -> Job:
        raise "Not Implemented"

    @staticmethod
    def job_to_event(
        job: Job,
        city: str | None = None,
        source: str | None = None,
    ) -> CanonicalJob:

        return CanonicalJob(
            title=job.title,
            company=job.company,
            description=job.description,
            city=city,
            meta={meta.key: meta.value for meta in job.meta if job.meta is not None},
            source=source,
            url=job.link,
            created_at=job.created_at,
        )
