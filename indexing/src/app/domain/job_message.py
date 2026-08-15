from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field

from app.domain.canonical_job import CanonicalJob


class JobMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()))

    message_type: str = "job.created"

    version: int = 1

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    job: CanonicalJob
