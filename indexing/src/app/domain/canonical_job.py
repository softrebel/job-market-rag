from datetime import datetime

from pydantic import BaseModel, Field


class CanonicalJob(BaseModel):
    id: str

    title: str

    company: str

    description: str

    city: str | None

    meta: dict[str, list[str]] = Field(default_factory=dict)

    source: str

    url: str

    content_hash: str | None = None

    created_at: datetime
