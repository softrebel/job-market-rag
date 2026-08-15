from unittest.mock import Mock

from app.domain.parsed_query import ParsedQuery
from app.domain.search_filters import SearchFilters
from app.domain.search_query import SearchQuery
from app.domain.search_result import SearchResult
from app.services.search_service import SearchService


def test_search_pipeline():

    parser = Mock()
    embedder = Mock()
    filter_builder = Mock()
    vectorstore = Mock()
    aggregator = Mock()

    parser.parse.return_value = ParsedQuery(
        semantic_query="Senior Python Developer",
        filters=SearchFilters(
            city=["تهران"],
        ),
    )

    embedder.embed_query.return_value = [
        0.1,
        0.2,
        0.3,
    ]

    filter_builder.build.return_value = "QDRANT_FILTER"

    vectorstore.search.return_value = [
        "POINT_1",
        "POINT_2",
    ]

    expected_results = [
        SearchResult(
            job_id="1",
            title="Senior Python Developer",
            company="Sedreh",
            text="Python Django Developer",
            city="تهران",
            source="jobinja",
            url="https://example.com",
            chunk_id="1_0",
            score=0.91,
            metadata={"skills": ["Python", "Django"]},
        )
    ]

    aggregator.aggregate.return_value = expected_results

    service = SearchService(
        parser=parser,
        embedder=embedder,
        filter_builder=filter_builder,
        vectorstore=vectorstore,
        aggregator=aggregator,
    )

    result = service.search(
        SearchQuery(
            query=("Senior Python Developer در تهران"),
            top_k=5,
        )
    )

    assert result == expected_results

    parser.parse.assert_called_once()

    embedder.embed_query.assert_called_once_with("Senior Python Developer")

    filter_builder.build.assert_called_once()

    vectorstore.search.assert_called_once_with(
        vector=[0.1, 0.2, 0.3],
        limit=5,
        query_filter="QDRANT_FILTER",
    )

    aggregator.aggregate.assert_called_once_with(["POINT_1", "POINT_2"])
