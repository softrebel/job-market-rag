from qdrant_client import QdrantClient
from qdrant_client.models import Filter, ScoredPoint


class QdrantVectorStore:
    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
    ):
        self.client = client
        self.collection_name = collection_name

    def search(
        self,
        vector: list[float],
        limit: int = 10,
        query_filter: Filter | None = None,
    ) -> list[ScoredPoint]:

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
        )

        return response.points
