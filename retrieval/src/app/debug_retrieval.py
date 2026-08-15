from app.container import create_retriever
from app.domain.search_query import SearchQuery


def main():

    retriever = create_retriever()

    query = SearchQuery(
        query="Senior Python Developer",
        top_k=10,
        filters={
            "city": ["تهران ، تهران"],
        },
    )

    results = retriever.retrieve(query)

    print()
    print("=" * 60)
    print(f"Query: {query.query}")
    print(f"Jobs: {len(results)}")
    print("=" * 60)

    for index, result in enumerate(
        results,
        start=1,
    ):
        print()
        print(f"[{index}]")
        print(f"Job ID: {result.job_id}")
        print(f"Title: {result.title}")
        print(f"Company: {result.company}")
        print(f"City: {result.city}")
        print(f"Score: {result.score:.4f}")
        print(f"Chunk: {result.chunk_id}")
        print(f"URL: {result.url}")


if __name__ == "__main__":
    main()
