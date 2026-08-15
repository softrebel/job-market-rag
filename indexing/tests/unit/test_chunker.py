from datetime import datetime

from app.chunking.job_chunker import JobChunker
from app.domain.canonical_job import CanonicalJob
from app.normalization.job_metadata import JobMetadataNormalizer


def make_job() -> CanonicalJob:
    return CanonicalJob(
        id="1",
        title="Senior Python Developer",
        company="Test Company",
        description=("Python backend developer with Django and PostgreSQL experience."),
        city="تهران",
        meta={
            "مهارت‌های مورد نیاز": [
                "Python",
                "Django",
                "PostgreSQL",
            ],
            "نوع همکاری": [
                "تمام وقت",
            ],
        },
        source="test",
        url="https://example.com",
        created_at=datetime.now(),
    )


def test_chunk_job():

    normalizer = JobMetadataNormalizer()

    chunker = JobChunker(
        normalizer=normalizer,
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.chunk(make_job())

    assert len(chunks) > 0

    assert chunks[0].job_id == "1"

    assert chunks[0].chunk_index == 0

    assert chunks[0].metadata.skills == [
        "Python",
        "Django",
        "PostgreSQL",
    ]

    assert chunks[0].text
