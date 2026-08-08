from datetime import datetime

from pydantic import BaseModel


class CanonicalJob(BaseModel):
    id: str

    title: str

    company: str

    description: str

    city: str | None

    meta: dict[str, list[str]] = {}

    source: str

    url: str

    content_hash: str | None = None

    created_at: datetime
