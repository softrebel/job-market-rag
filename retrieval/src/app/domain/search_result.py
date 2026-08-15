from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    job_id: str

    title: str
    company: str

    text: str | None = None
    city: str | None = None

    score: float

    source: str | None = None
    url: str | None = None

    chunk_id: str | None = None

    metadata: dict = Field(default_factory=dict)
