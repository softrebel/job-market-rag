from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalConfig:
    candidate_limit: int = 50
