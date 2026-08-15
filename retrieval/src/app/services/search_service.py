from app.domain.parsed_query import ParsedQuery
from app.domain.search_query import SearchQuery
from app.domain.search_result import SearchResult
from app.embeddings.base import BaseEmbedder
from app.query.parser import QueryParser
from app.retrieval.aggregator import JobResultAggregator
from app.retrieval.filters import QdrantFilterBuilder
from app.retrieval.ranker import JobRanker
from app.vectorstore.qdrant import QdrantVectorStore


class SearchService:
    def __init__(
        self,
        parser: QueryParser,
        embedder: BaseEmbedder,
        filter_builder: QdrantFilterBuilder,
        vectorstore: QdrantVectorStore,
        aggregator: JobResultAggregator,
        ranker: JobRanker,
        candidate_multiplier: int = 5,
    ):
        self.parser = parser
        self.embedder = embedder
        self.filter_builder = filter_builder
        self.vectorstore = vectorstore
        self.aggregator = aggregator
        self.ranker = ranker
        self.candidate_multiplier = candidate_multiplier

    def search(
        self,
        query: SearchQuery,
    ) -> list[SearchResult]:

        parsed: ParsedQuery = self.parser.parse(query.query)

        semantic_query = parsed.semantic_query

        query_vector = self.embedder.embed_query(semantic_query)

        qdrant_filter = self.filter_builder.build(parsed.filters)

        candidate_limit = min(
            query.top_k * self.candidate_multiplier,
            100,
        )

        points = self.vectorstore.search(
            vector=query_vector,
            limit=candidate_limit,
            query_filter=qdrant_filter,
        )

        ranked_points = self.ranker.rank(
            points=points,
            query=semantic_query,
            top_k=query.top_k,
        )

        return self.aggregator.aggregate(ranked_points)
