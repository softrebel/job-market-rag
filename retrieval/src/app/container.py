from qdrant_client import QdrantClient

from app.config.settings import settings
from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)
from app.vectorstore.qdrant import QdrantVectorStore
from app.retrieval.semantic import SemanticRetriever
from app.retrieval.aggregator import JobResultAggregator
from app.retrieval.filters import QdrantFilterBuilder

from app.query.parser import QueryParser
from app.services.search_service import SearchService
from app.retrieval.config import RetrievalConfig
from app.retrieval.ranker import JobRanker
from functools import lru_cache


@lru_cache
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
    )


@lru_cache
def get_embedder() -> SentenceTransformerEmbedder:
    return SentenceTransformerEmbedder(
        model_name=settings.embedding_model,
    )


@lru_cache
def get_vectorstore() -> QdrantVectorStore:

    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=settings.qdrant_collection,
    )


@lru_cache
def get_query_parser() -> QueryParser:
    return QueryParser()


@lru_cache
def get_filter_builder() -> QdrantFilterBuilder:
    return QdrantFilterBuilder()


@lru_cache
def get_aggregator() -> JobResultAggregator:
    return JobResultAggregator()


@lru_cache
def get_job_ranker() -> JobRanker:
    return JobRanker()


@lru_cache
def get_retrieval_config() -> RetrievalConfig:
    return RetrievalConfig()


@lru_cache
def get_search_service() -> SearchService:

    return SearchService(
        parser=get_query_parser(),
        embedder=get_embedder(),
        filter_builder=get_filter_builder(),
        vectorstore=get_vectorstore(),
        aggregator=get_aggregator(),
        ranker=get_job_ranker(),
    )


def create_retriever() -> SemanticRetriever:

    embedder = SentenceTransformerEmbedder(settings.embedding_model)

    qdrant_client = QdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
    )

    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name=settings.qdrant_collection,
    )
    aggregator = JobResultAggregator()
    filter_builder = QdrantFilterBuilder()

    return SemanticRetriever(
        embedder=embedder,
        vectorstore=vectorstore,
        aggregator=aggregator,
        filter_builder=filter_builder,
    )
