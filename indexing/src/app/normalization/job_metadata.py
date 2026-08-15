from app.domain.canonical_job import CanonicalJob
from app.domain.indexed_job import IndexedJobMetadata


class JobMetadataNormalizer:
    META_MAPPING = {
        "مهارت‌های مورد نیاز": "skills",
        "دسته‌بندی شغلی": "job_category",
        "حقوق": "salary",
        "جنسیت": "gender",
        "نوع همکاری": "employment_type",
        "حداقل مدرک تحصیلی": "education",
        "وضعیت نظام وظیفه": "military_service",
        "حداقل سابقه کار": "experience",
    }

    def normalize(
        self,
        job: CanonicalJob,
    ) -> IndexedJobMetadata:

        normalized = {
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "city": job.city,
            "source": job.source,
            "url": job.url,
            "content_hash": job.content_hash,
        }

        source_meta = {}

        for source_key, values in job.meta.items():
            target_key = self.META_MAPPING.get(source_key)

            if target_key is None:
                source_meta[source_key] = values
                continue

            normalized[target_key] = values

        normalized["source_meta"] = source_meta

        return IndexedJobMetadata(**normalized)
