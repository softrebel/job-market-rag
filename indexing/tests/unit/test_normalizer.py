from datetime import datetime

from app.domain.canonical_job import CanonicalJob
from app.normalization.job_metadata import JobMetadataNormalizer


def test_normalize_job_metadata():

    job = CanonicalJob(
        id="1",
        title="Senior Python Developer",
        company="Test Company",
        description="Python backend developer",
        city="تهران",
        meta={
            "مهارت‌های مورد نیاز": [
                "Python",
                "Django",
            ],
            "نوع همکاری": [
                "تمام وقت",
            ],
            "حداقل سابقه کار": [
                "سه تا شش سال",
            ],
            "موقعیت مکانی": [
                "تهران",
            ],
        },
        source="jobinja",
        url="https://example.com/job/1",
        content_hash="abc",
        created_at=datetime.now(),
    )

    normalizer = JobMetadataNormalizer()

    result = normalizer.normalize(job)

    assert result.job_id == "1"
    assert result.title == "Senior Python Developer"
    assert result.company == "Test Company"

    assert result.skills == [
        "Python",
        "Django",
    ]

    assert result.employment_type == [
        "تمام وقت",
    ]

    assert result.experience == [
        "سه تا شش سال",
    ]

    # چون mapping نشده
    assert result.source_meta == {"موقعیت مکانی": ["تهران"]}
