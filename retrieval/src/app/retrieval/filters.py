from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchAny,
    MatchText,
    Range,
)

from app.domain.search_filters import SearchFilters


class QdrantFilterBuilder:
    def build(
        self,
        filters: SearchFilters,
    ) -> Filter | None:

        must: list = []

        self._add_or_text_filter(
            must,
            "city",
            filters.city,
        )

        self._add_or_text_filter(
            must,
            "company",
            filters.company,
        )

        self._add_and_text_filter(
            must,
            "skills",
            filters.skills,
        )

        self._add_or_text_filter(
            must,
            "categories",
            filters.categories,
        )

        self._add_or_exact_filter(
            must,
            "source",
            filters.source,
        )

        self._add_or_exact_filter(
            must,
            "employment_type",
            filters.employment_type,
        )

        self._add_or_exact_filter(
            must,
            "gender",
            filters.gender,
        )

        if filters.experience_min is not None:
            must.append(
                FieldCondition(
                    key="experience_years",
                    range=Range(gte=filters.experience_min),
                )
            )

        if filters.experience_max is not None:
            must.append(
                FieldCondition(
                    key="experience_years",
                    range=Range(lte=filters.experience_max),
                )
            )

        if not must:
            return None

        return Filter(must=must)

    @staticmethod
    def _add_or_text_filter(
        conditions: list,
        field: str,
        values: list[str],
    ) -> None:

        if not values:
            return

        conditions.append(
            Filter(
                should=[
                    FieldCondition(
                        key=field,
                        match=MatchText(
                            text=value,
                        ),
                    )
                    for value in values
                ],
            )
        )

    @staticmethod
    def _add_and_text_filter(
        conditions: list,
        field: str,
        values: list[str],
    ) -> None:

        if not values:
            return

        for value in values:
            conditions.append(
                FieldCondition(
                    key=field,
                    match=MatchText(
                        text=value,
                    ),
                )
            )

    @staticmethod
    def _add_or_exact_filter(
        conditions: list,
        field: str,
        values: list[str],
    ) -> None:

        if not values:
            return

        conditions.append(
            FieldCondition(
                key=field,
                match=MatchAny(any=values),
            )
        )
