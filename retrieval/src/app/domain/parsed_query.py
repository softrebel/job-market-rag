from pydantic import BaseModel, Field

from app.domain.search_filters import SearchFilters


class ParsedQuery(BaseModel):
    semantic_query: str

    filters: SearchFilters
