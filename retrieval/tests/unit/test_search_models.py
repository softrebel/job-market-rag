from app.domain.search_query import SearchQuery
from app.domain.search_result import SearchResult


def test_search_query_defaults():

    query = SearchQuery(query="Python developer")

    assert query.query == "Python developer"
    assert query.top_k == 10
    assert query.filters == {}


def test_search_query_with_filters():

    query = SearchQuery(
        query="Python developer",
        top_k=20,
        filters={
            "city": ["تهران"],
        },
    )

    assert query.top_k == 20
    assert query.filters["city"] == ["تهران"]


def test_search_result():

    result = SearchResult(
        job_id="1",
        title="Senior Backend Developer",
        company="Sedreh",
        score=0.87,
    )

    assert result.job_id == "1"
    assert result.score == 0.87
