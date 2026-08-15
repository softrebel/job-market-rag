import logging

import redis
from qdrant_client import QdrantClient

from app.chunking.job_chunker import JobChunker
from app.config.settings import settings
from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)
from app.messaging.redis_consumer import RedisStreamConsumer
from app.normalization.job_metadata import JobMetadataNormalizer
from app.pipeline.indexer import JobIndexer
from app.vectorstore.qdrant import QdrantVectorStore
from app.worker.indexing_worker import IndexingWorker


def setup_logging() -> None:

    logging.basicConfig(
        level=getattr(
            logging,
            settings.LOG_LEVEL.upper(),
            logging.INFO,
        ),
        format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
    )


def build_worker() -> IndexingWorker:

    # ------------------------------------------
    # Redis
    # ------------------------------------------

    redis_client = redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=False,
        socket_connect_timeout=5,
        socket_timeout=None,
        health_check_interval=30,
    )

    consumer = RedisStreamConsumer(
        client=redis_client,
        stream_name=settings.REDIS_STREAM_NAME,
        group_name=settings.REDIS_CONSUMER_GROUP,
        consumer_name=settings.REDIS_CONSUMER_NAME,
    )

    # ------------------------------------------
    # Normalization
    # ------------------------------------------

    normalizer = JobMetadataNormalizer()

    # ------------------------------------------
    # Chunking
    # ------------------------------------------

    chunker = JobChunker(
        normalizer=normalizer,
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )

    # ------------------------------------------
    # Embedding
    # ------------------------------------------

    embedder = SentenceTransformerEmbedder()

    # ------------------------------------------
    # Qdrant
    # ------------------------------------------

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

    # ------------------------------------------
    # Indexer
    # ------------------------------------------

    indexer = JobIndexer(
        chunker=chunker,
        embedder=embedder,
        vectorstore=vectorstore,
    )

    # ------------------------------------------
    # Worker
    # ------------------------------------------

    return IndexingWorker(
        consumer=consumer,
        indexer=indexer,
    )


def main() -> None:

    setup_logging()

    logger = logging.getLogger(__name__)

    logger.info("Starting Job Market Indexing Service")

    worker = build_worker()

    worker.run()


if __name__ == "__main__":
    main()
