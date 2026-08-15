from fastapi import APIRouter, Depends

from app.api.schemas import (
    SearchRequest,
    SearchResponse,
)
from app.container import get_search_service
from app.domain.search_query import SearchQuery
from app.services.search_service import SearchService


router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.post(
    "",
    response_model=SearchResponse,
)
def search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),
) -> SearchResponse:

    query = SearchQuery(
        query=request.query,
        top_k=request.top_k,
        filters=request.filters,
    )

    results = service.search(query)

    return SearchResponse(results=results)
