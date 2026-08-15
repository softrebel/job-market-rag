from app.domain.search_query import SearchQuery
from app.domain.search_result import SearchResult
from app.embeddings.base import BaseEmbedder
from app.retrieval.aggregator import JobResultAggregator
from app.retrieval.filters import QdrantFilterBuilder
from app.vectorstore.qdrant import QdrantVectorStore


class SemanticRetriever:
    def __init__(
        self,
        embedder: BaseEmbedder,
        vectorstore: QdrantVectorStore,
        aggregator: JobResultAggregator,
        filter_builder: QdrantFilterBuilder,
    ):
        self.embedder = embedder
        self.vectorstore = vectorstore
        self.aggregator = aggregator
        self.filter_builder = filter_builder

    def retrieve(
        self,
        search_query: SearchQuery,
    ) -> list[SearchResult]:

        query_vector = self.embedder.embed_query(search_query.query)

        query_filter = self.filter_builder.build(search_query.filters)

        points = self.vectorstore.search(
            vector=query_vector,
            limit=search_query.top_k,
            query_filter=query_filter,
        )

        return self.aggregator.aggregate(points)
