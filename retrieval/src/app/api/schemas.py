from pydantic import BaseModel, Field

from app.domain.search_filters import SearchFilters
from app.domain.search_result import SearchResult


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)

    top_k: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    filters: SearchFilters = Field(default_factory=SearchFilters)


class SearchResponse(BaseModel):
    results: list[SearchResult]
