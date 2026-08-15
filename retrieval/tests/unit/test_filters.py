from qdrant_client.models import MatchText
from qdrant_client.models import FieldCondition

from app.domain.search_filters import SearchFilters
from app.retrieval.filters import QdrantFilterBuilder



def test_city_values_are_or():
    builder = QdrantFilterBuilder()

    filters = SearchFilters(
        city=["تهران", "کرج"],
    )

    result = builder.build(filters)

    assert result is not None
    assert len(result.must) == 1

    city_filter = result.must[0]

    assert city_filter.should is not None
    assert len(city_filter.should) == 2


def test_skills_values_are_and():
    builder = QdrantFilterBuilder()

    filters = SearchFilters(
        skills=["Python", "Django"],
    )

    result = builder.build(filters)

    assert result is not None
    assert len(result.must) == 2

    assert all(
        isinstance(
            condition,
            FieldCondition,
        )
        for condition in result.must
    )


def test_different_filter_groups_are_and():
    builder = QdrantFilterBuilder()

    filters = SearchFilters(
        city=["تهران", "کرج"],
        skills=["Python", "Django"],
        source=["jobinja", "linkedin"],
        experience_min=3,
    )

    result = builder.build(filters)

    assert result is not None

    # city + skills(2) + source + experience
    assert len(result.must) == 5
