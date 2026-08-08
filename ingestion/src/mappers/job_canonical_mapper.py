from database.session import Job

from domain.canonical_job import CanonicalJob


class CanonicalJobMapper:
    @staticmethod
    def canonical_to_job(canonical: CanonicalJob) -> Job:
        raise "Not Implemented"

    @staticmethod
    def job_to_canonical(
        job: Job,
    ) -> CanonicalJob:

        city = None
        source = None
        # meta = {
        #     meta.key: meta.value
        #     for meta in job.jobmeta_collection
        #     if job.jobmeta_collection is not None
        # }

        meta = {
            key: [str(item.value) for item in job.jobmeta_collection if item.key == key]
            for key in {item.key for item in job.jobmeta_collection}
            if job.jobmeta_collection is not None
        }
        if len(meta.keys()) > 0:
            city = next(
                value[0]
                for key, value in meta.items()
                if key == "city" or "مکان" in key
            )
        source = job.jobplatform.name if job.jobplatform else None

        return CanonicalJob(
            id=str(job.id),
            title=job.title,
            company=job.company.name,
            description=job.description,
            city=city,
            meta=meta,
            source=source,
            url=job.link,
            created_at=job.created_at,
        )
