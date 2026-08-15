from qdrant_client.models import ScoredPoint

from app.retrieval.aggregator import JobResultAggregator


def make_point(
    point_id: str,
    job_id: str,
    score: float,
    title: str = "Python Developer",
):
    return ScoredPoint(
        id=point_id,
        version=1,
        score=score,
        payload={
            "job_id": job_id,
            "title": title,
            "company": "Test Company",
            "city": "Tehran",
            "source": "jobinja",
            "url": "https://example.com",
        },
    )


def test_aggregate_removes_duplicate_jobs():

    points = [
        make_point(
            "chunk-1",
            "job-1",
            0.91,
        ),
        make_point(
            "chunk-2",
            "job-1",
            0.85,
        ),
        make_point(
            "chunk-3",
            "job-2",
            0.88,
        ),
    ]

    aggregator = JobResultAggregator()

    results = aggregator.aggregate(points)

    assert len(results) == 2

    assert results[0].job_id == "job-1"
    assert results[0].score == 0.91

    assert results[1].job_id == "job-2"
    assert results[1].score == 0.88


def test_aggregate_keeps_best_chunk():

    points = [
        make_point(
            "chunk-1",
            "job-1",
            0.70,
        ),
        make_point(
            "chunk-2",
            "job-1",
            0.95,
        ),
        make_point(
            "chunk-3",
            "job-1",
            0.80,
        ),
    ]

    aggregator = JobResultAggregator()

    results = aggregator.aggregate(points)

    assert len(results) == 1
    assert results[0].score == 0.95
    assert results[0].chunk_id == "chunk-2"
