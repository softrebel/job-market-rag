from qdrant_client.models import ScoredPoint

from app.retrieval.ranker import JobRanker


def make_point(
    point_id: str,
    semantic_score: float,
    title: str,
    skills: list[str],
):
    return ScoredPoint(
        id=point_id,
        version=1,
        score=semantic_score,
        payload={
            "title": title,
            "description": "",
            "skills": skills,
        },
    )


def test_title_match_improves_ranking():

    points = [
        make_point(
            point_id="1",
            semantic_score=0.90,
            title="Frontend Developer",
            skills=["JavaScript"],
        ),
        make_point(
            point_id="2",
            semantic_score=0.80,
            title="Python Backend Developer",
            skills=["Python", "Django"],
        ),
    ]

    ranker = JobRanker()

    results = ranker.rank(
        points=points,
        query="Python Developer",
        top_k=2,
    )

    assert str(results[0].id) == "2"


def test_skill_alias_improves_ranking():

    points = [
        make_point(
            point_id="1",
            semantic_score=0.90,
            title="Backend Developer",
            skills=["Java"],
        ),
        make_point(
            point_id="2",
            semantic_score=0.80,
            title="Backend Developer",
            skills=["Python3"],
        ),
    ]

    ranker = JobRanker()

    results = ranker.rank(
        points=points,
        query="Python",
        top_k=2,
    )

    assert str(results[0].id) == "2"
