from enum import StrEnum


class FilterType(StrEnum):
    EXACT = "exact"
    TEXT = "text"
    ANY = "any"
    ALL = "all"


FILTER_TYPES: dict[str, FilterType] = {
    # Text / contains
    "city": FilterType.TEXT,
    "company": FilterType.TEXT,
    "title": FilterType.TEXT,
    # Exact
    "source": FilterType.EXACT,
    "employment_type": FilterType.EXACT,
    "gender": FilterType.EXACT,
    # Array fields
    "skills": FilterType.ANY,
    "categories": FilterType.ANY,
}
