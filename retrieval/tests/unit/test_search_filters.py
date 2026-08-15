from app.domain.search_filters import SearchFilters


def test_merge_filters():
    parsed = SearchFilters(
        city=["تهران"],
    )

    explicit = SearchFilters(
        experience_min=3,
    )

    result = parsed.merge(explicit)

    assert result.city == ["تهران"]
    assert result.experience_min == 3


def test_merge_filters_combines_lists():
    parsed = SearchFilters(
        city=["تهران"],
        skills=["Python"],
    )

    explicit = SearchFilters(
        company=["Sedreh"],
        skills=["Django"],
    )

    result = parsed.merge(explicit)

    assert result.city == ["تهران"]
    assert result.company == ["Sedreh"]
    assert result.skills == ["Python", "Django"]
