import hashlib

from domain.canonical_job import CanonicalJob


class HashService:
    @staticmethod
    def generate(
        job: CanonicalJob,
    ) -> str:

        value = "|".join(
            [
                job.title.strip(),
                job.company.strip(),
                job.url.strip(),
            ]
        )

        return hashlib.sha256(value.encode("utf-8")).hexdigest()
