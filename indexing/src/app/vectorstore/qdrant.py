from collections.abc import Sequence


from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.domain.chunk import JobChunk


class QdrantVectorStore:
    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
        vector_size: int,
    ):
        self.client = client
        self.collection_name = collection_name
        self.vector_size = vector_size

    def delete_by_job_id(
        self,
        job_id: str,
    ) -> None:

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="job_id",
                        match=MatchValue(
                            value=job_id,
                        ),
                    )
                ]
            ),
            wait=True,
        )

    def create_collection(self) -> None:

        collections = self.client.get_collections()

        exists = any(
            collection.name == self.collection_name
            for collection in collections.collections
        )

        if exists:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert(
        self,
        chunks: Sequence[JobChunk],
        vectors: Sequence[Sequence[float]],
    ) -> None:

        if len(chunks) != len(vectors):
            raise ValueError("Number of chunks and vectors must be equal.")

        points = []

        for chunk, vector in zip(
            chunks,
            vectors,
            strict=True,
        ):
            points.append(
                PointStruct(
                    id=chunk.chunk_id,
                    vector=list(vector),
                    payload={
                        "job_id": chunk.job_id,
                        "chunk_index": chunk.chunk_index,
                        "text": chunk.text,
                        **chunk.metadata,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )
