from app.chunking.job_chunker import JobChunker
from app.domain.canonical_job import CanonicalJob
from app.embeddings.base import BaseEmbedder
from app.vectorstore.qdrant import QdrantVectorStore


class JobIndexer:
    def __init__(
        self,
        chunker: JobChunker,
        embedder: BaseEmbedder,
        vectorstore: QdrantVectorStore,
    ):
        self.chunker = chunker
        self.embedder = embedder
        self.vectorstore = vectorstore

    def index(
        self,
        job: CanonicalJob,
    ) -> int:

        # Remove previously indexed chunks
        # belonging to this job.
        # self.vectorstore.delete_by_job_id(job.id)

        chunks = self.chunker.chunk(job)

        if not chunks:
            return 0

        texts = [chunk.text for chunk in chunks]

        vectors = self.embedder.embed(texts)

        self.vectorstore.upsert(
            chunks,
            vectors,
        )

        return len(chunks)
