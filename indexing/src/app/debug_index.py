from datetime import datetime

from qdrant_client import QdrantClient

from app.chunking.job_chunker import JobChunker
from app.config.settings import settings
from app.domain.canonical_job import CanonicalJob
from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)
from app.normalization.job_metadata import JobMetadataNormalizer
from app.pipeline.indexer import JobIndexer
from app.vectorstore.qdrant import QdrantVectorStore


def main():

    job = CanonicalJob(
        id="debug-1",
        title="Senior Back-End Developer",
        company="Sedreh",
        description=(
            "شرکت ویراپردازان سدره به دنبال "
            "Senior Back-End Developer است. "
            "تسلط به Python، Django، PostgreSQL، "
            "Docker، Redis و Celery مورد نیاز است."
        ),
        city="تهران",
        meta={
            "مهارت‌های مورد نیاز": [
                "Python",
                "Django",
                "PostgreSQL",
                "Redis",
                "Celery",
            ],
            "نوع همکاری": [
                "تمام وقت",
            ],
            "حداقل سابقه کار": [
                "سه تا شش سال",
            ],
        },
        source="debug",
        url="https://example.com/debug",
        content_hash="debug-hash",
        created_at=datetime.now(),
    )

    normalizer = JobMetadataNormalizer()

    chunker = JobChunker(
        normalizer=normalizer,
    )

    embedder = SentenceTransformerEmbedder()

    qdrant_client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY or None,
    )

    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        vector_size=embedder.dimension,
    )

    vectorstore.create_collection()

    indexer = JobIndexer(
        chunker=chunker,
        embedder=embedder,
        vectorstore=vectorstore,
    )

    indexer.index(job)

    print("Job indexed successfully.")
    print("Embedding dimension:", embedder.dimension)


if __name__ == "__main__":
    main()
