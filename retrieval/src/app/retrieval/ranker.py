from qdrant_client.models import ScoredPoint

from app.retrieval.ranking_config import RankingConfig
from app.retrieval.skill_normalizer import SkillNormalizer
from app.retrieval.text_normalizer import TextNormalizer


class JobRanker:
    def __init__(
        self,
        config: RankingConfig | None = None,
    ):
        self.config = config or RankingConfig()

    def rank(
        self,
        points: list[ScoredPoint],
        query: str,
        top_k: int,
    ) -> list[ScoredPoint]:

        query_tokens = TextNormalizer.tokenize(query)

        scored: list[tuple[float, ScoredPoint]] = []

        for point in points:
            payload = point.payload or {}

            title = str(payload.get("title", ""))

            description = str(payload.get("description", ""))

            skills = payload.get(
                "skills",
                [],
            )

            score = self._calculate_score(
                semantic_score=point.score,
                query_tokens=query_tokens,
                title=title,
                description=description,
                skills=skills,
            )

            scored.append((score, point))

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [point for _, point in scored[:top_k]]

    def _calculate_score(
        self,
        semantic_score: float,
        query_tokens: set[str],
        title: str,
        description: str,
        skills: list[str],
    ) -> float:

        title_tokens = TextNormalizer.tokenize(title)

        description_tokens = TextNormalizer.tokenize(description)

        skill_tokens = SkillNormalizer.normalize_many(skills)

        title_score = self._overlap(
            query_tokens,
            title_tokens,
        )

        skills_score = self._skill_overlap(
            query_tokens,
            skill_tokens,
        )

        description_score = self._overlap(
            query_tokens,
            description_tokens,
        )

        config = self.config

        return (
            config.semantic_weight * semantic_score
            + config.title_weight * title_score
            + config.skills_weight * skills_score
            + config.description_weight * description_score
        )

    @staticmethod
    def _overlap(
        query_tokens: set[str],
        document_tokens: set[str],
    ) -> float:

        if not query_tokens:
            return 0.0

        return len(query_tokens & document_tokens) / len(query_tokens)

    @staticmethod
    def _skill_overlap(
        query_tokens: set[str],
        skill_tokens: set[str],
    ) -> float:

        if not query_tokens:
            return 0.0

        matched = 0

        for token in query_tokens:
            if token in skill_tokens:
                matched += 1

        return matched / len(query_tokens)
