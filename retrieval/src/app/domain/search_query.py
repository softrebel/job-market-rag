from pydantic import BaseModel, Field

from app.domain.search_filters import SearchFilters


class SearchQuery(BaseModel):
    query: str = Field(min_length=1)

    top_k: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    filters: SearchFilters = Field(default_factory=SearchFilters)
