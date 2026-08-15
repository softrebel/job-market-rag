from fastapi.testclient import TestClient

from app.container import get_search_service
from app.domain.search_filters import SearchFilters
from app.domain.search_query import SearchQuery
from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)
from app.main import app
from app.query.parser import QueryParser
from app.retrieval.aggregator import JobResultAggregator
from app.retrieval.filters import QdrantFilterBuilder
from app.services.search_service import SearchService
from app.vectorstore.qdrant import QdrantVectorStore

from tests.fixtures.qdrant import (
    EMBEDDING_MODEL,
    TEST_COLLECTION,
)
from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchText,
)

client = TestClient(app)


def test_search_service_city_debug(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    query = SearchQuery(
        query="Python Developer در تهران",
        top_k=10,
    )

    parsed = service.parser.parse(query.query)

    print("\nPARSED QUERY:")
    print("semantic_query:", parsed.semantic_query)
    print("filters:", parsed.filters)
    print("city:", parsed.filters.city)

    qdrant_filter = service.filter_builder.build(parsed.filters)

    print("\nQDRANT FILTER:")
    print(qdrant_filter)

    results = service.search(query)

    print("\nRESULTS:")
    for result in results:
        print(
            result.job_id,
            result.city,
            result.title,
        )

    assert parsed.filters.city == ["تهران"]

    assert all(result.city and "تهران" in result.city for result in results)


def test_qdrant_city_filter(
    qdrant_client,
    test_data,
):
    result, _ = qdrant_client.scroll(
        collection_name=TEST_COLLECTION,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="city",
                    match=MatchText(
                        text="تهران",
                    ),
                )
            ]
        ),
        limit=10,
    )

    cities = [point.payload["city"] for point in result]

    print("CITIES:", cities)

    assert cities

    assert all("تهران" in city for city in cities)


def build_test_service(qdrant_client):
    embedder = SentenceTransformerEmbedder(
        model_name=EMBEDDING_MODEL,
    )

    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name=TEST_COLLECTION,
    )

    return SearchService(
        parser=QueryParser(),
        embedder=embedder,
        filter_builder=QdrantFilterBuilder(),
        vectorstore=vectorstore,
        aggregator=JobResultAggregator(),
    )


def test_search_api(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    app.dependency_overrides[get_search_service] = lambda: service

    client = TestClient(app)

    response = client.post(
        "/search",
        json={
            "query": "Senior Python Developer",
            "top_k": 5,
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert len(data["results"]) > 0


def test_search_with_city_filter(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    query = SearchQuery(
        query="Python Developer",
        top_k=10,
        filters=SearchFilters(
            city=["تهران"],
        ),
    )

    results = service.search(query)

    assert len(results) > 0

    for result in results:
        assert result.city is not None
        assert "تهران" in result.city


def test_city_filter_excludes_other_cities(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    query = SearchQuery(
        query="Python Developer",
        top_k=10,
        filters=SearchFilters(
            city=["تهران"],
        ),
    )

    results = service.search(query)

    assert all(result.city and "تهران" in result.city for result in results)

    assert all(result.job_id != "3" for result in results)


def test_search_without_filter(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    query = SearchQuery(
        query="Python Developer",
        top_k=10,
    )

    results = service.search(query)

    assert len(results) > 0


def test_semantic_search_returns_python_jobs(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    query = SearchQuery(
        query="برنامه نویس پایتون بک اند",
        top_k=3,
    )

    results = service.search(query)

    assert len(results) > 0

    job_ids = {result.job_id for result in results}

    assert "1" in job_ids


def test_city_filter_uses_or(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    query = SearchQuery(
        query="Developer",
        top_k=10,
        filters=SearchFilters(
            city=["تهران", "کرج"],
        ),
    )

    results = service.search(query)

    assert results

    assert all(
        result.city and ("تهران" in result.city or "کرج" in result.city)
        for result in results
    )


def test_skills_filter_uses_and(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    query = SearchQuery(
        query="Developer",
        top_k=10,
        filters=SearchFilters(
            skills=["Python", "Django"],
        ),
    )

    results = service.search(query)

    assert results

    for result in results:
        skills = result.metadata.get("skills", [])

        normalized_skills = {skill.lower() for skill in skills}

        assert "python" in normalized_skills
        assert "django" in normalized_skills


def test_filter_groups_are_combined_with_and(
    qdrant_client,
    test_data,
):
    service = build_test_service(qdrant_client)

    query = SearchQuery(
        query="Developer",
        top_k=10,
        filters=SearchFilters(
            city=["تهران"],
            source=["jobinja"],
        ),
    )

    results = service.search(query)

    assert results

    for result in results:
        assert result.city
        assert "تهران" in result.city
        assert result.source == "jobinja"
