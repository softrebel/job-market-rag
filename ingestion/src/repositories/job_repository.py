from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, selectinload

# from database.models import JobModel
from database.session import Job


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, job: Job) -> Job:
        """
        Create a new job.
        """

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def get(self, job_id: int) -> Job | None:
        """
        Get a job by primary key.
        """

        return self.db.get(Job, job_id)

    def get_by_hash(self, content_hash: str) -> Job | None:
        """
        Find job by content hash.
        """

        stmt = select(Job).where(Job.content_hash == content_hash)

        return self.db.scalar(stmt)

    def exists(self, content_hash: str) -> bool:
        """
        Check duplicate job.
        """

        return self.get_by_hash(content_hash) is not None

    def get_all(self) -> list["Job"]:
        """
        Return all jobs.
        """

        stmt = select(Job)

        return list(self.db.scalars(stmt).all())

    def delete(self, job: Job) -> None:
        """
        Delete a job.
        """

        self.db.delete(job)
        self.db.commit()

    def fetch_jobs_batch(
        self, last_id: int, batch_size: int = 500
    ) -> list["Job"] | None:
        stmt = (
            select(Job)
            .options(
                joinedload(Job.company),
                joinedload(Job.jobplatform),
                selectinload(Job.jobmeta_collection),
            )
            .where(Job.id > last_id)
            .order_by(Job.id)
            .limit(batch_size)
        )

        jobs = self.db.scalars(stmt).all()

        return jobs
