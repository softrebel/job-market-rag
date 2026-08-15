from app.domain.search_query import SearchQuery
from app.services.search_service import SearchService
from app.container import build_search_service


def main(query):

    print(f"query: {query}")
    service = build_search_service()

    query = SearchQuery(
        query=query,
        top_k=5,
    )

    results = service.search(query)

    for result in results:
        print("=" * 60)

        print(f"{result.title} | {result.company}")

        print(f"City: {result.city}")

        print(f"Score: {result.score:.4f}")

        print(result.text[:300])


if __name__ == "__main__":
    main("Senior Python Developer در تهران با حداقل 3 سال سابقه")
    main("Senior Python Developer در تهران ")
