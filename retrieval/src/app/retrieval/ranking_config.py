from dataclasses import dataclass


@dataclass(frozen=True)
class RankingConfig:
    semantic_weight: float = 0.60
    title_weight: float = 0.20
    skills_weight: float = 0.15
    description_weight: float = 0.05
