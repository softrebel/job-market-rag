import re

from app.domain.parsed_query import ParsedQuery
from app.domain.search_filters import SearchFilters


class QueryParser:
    CITY_PATTERN = re.compile(r"(?:در|شهر)\s+([^\s،,]+)")

    EXPERIENCE_PATTERN = re.compile(
        r"(?:با\s+)?(?:حداقل|بیش از)\s*(\d+)\s*سال"
        r"(?:\s*سابقه)?"
    )

    def parse(
        self,
        query: str,
    ) -> ParsedQuery:

        filters = SearchFilters()

        semantic_query = query

        city_match = self.CITY_PATTERN.search(query)

        if city_match:
            filters.city = [city_match.group(1)]

            semantic_query = semantic_query.replace(
                city_match.group(0),
                "",
            )

        experience_match = self.EXPERIENCE_PATTERN.search(query)

        if experience_match:
            filters.experience_min = int(experience_match.group(1))

            semantic_query = semantic_query.replace(
                experience_match.group(0),
                "",
            )

        semantic_query = " ".join(semantic_query.split()).strip()

        return ParsedQuery(
            semantic_query=semantic_query,
            filters=filters,
        )
