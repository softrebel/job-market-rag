from app.config.settings import settings
from app.domain.canonical_job import CanonicalJob
from app.domain.chunk import JobChunk
from app.normalization.job_metadata import JobMetadataNormalizer
from app.utils.ids import make_chunk_id


class JobChunker:
    def __init__(
        self,
        normalizer: JobMetadataNormalizer,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        self.normalizer = normalizer

        self.chunk_size = chunk_size if chunk_size is not None else settings.CHUNK_SIZE

        self.chunk_overlap = (
            chunk_overlap if chunk_overlap is not None else settings.CHUNK_OVERLAP
        )

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

    def chunk(
        self,
        job: CanonicalJob,
    ) -> list[JobChunk]:

        metadata = self.normalizer.normalize(job)

        document = self._build_document(
            job,
            metadata,
        )

        texts = self._split_text(document)

        return [
            JobChunk(
                # chunk_id=f"{job.id}:{index}",
                chunk_id=make_chunk_id(
                    job_id=job.id,
                    chunk_index=index,
                    content_hash=job.content_hash,
                ),
                job_id=job.id,
                text=text,
                chunk_index=index,
                metadata=metadata,
                
            )
            for index, text in enumerate(texts)
        ]

    def _build_document(
        self,
        job: CanonicalJob,
        metadata,
    ) -> str:

        parts = [
            f"عنوان شغل: {job.title}",
            f"شرکت: {job.company}",
        ]

        if metadata.city:
            parts.append(f"شهر: {metadata.city}")

        if metadata.skills:
            parts.append("مهارت‌های مورد نیاز: " + ", ".join(metadata.skills))

        if metadata.job_category:
            parts.append("دسته‌بندی شغلی: " + ", ".join(metadata.job_category))

        if metadata.salary:
            parts.append("حقوق: " + ", ".join(metadata.salary))

        if metadata.employment_type:
            parts.append("نوع همکاری: " + ", ".join(metadata.employment_type))

        if metadata.education:
            parts.append("حداقل مدرک تحصیلی: " + ", ".join(metadata.education))

        if metadata.experience:
            parts.append("حداقل سابقه کار: " + ", ".join(metadata.experience))

        parts.extend(
            [
                "",
                "توضیحات شغل:",
                job.description,
            ]
        )

        return "\n".join(parts)

    def _split_text(
        self,
        text: str,
    ) -> list[str]:

        if len(text) <= self.chunk_size:
            return [text]

        chunks: list[str] = []

        start = 0

        while start < len(text):
            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start = end - self.chunk_overlap

        return chunks
