from pydantic import BaseModel, Field

from app.domain.search_result import SearchResult


class SearchResponse(BaseModel):
    query: str

    results: list[SearchResult] = Field(default_factory=list)

    total: int = 0
