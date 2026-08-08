from dataclasses import dataclass

from domain.canonical_job import CanonicalJob


@dataclass(slots=True)
class PipelineContext:
    canonical_job: CanonicalJob

    # content_hash: str | None = None

    @property
    def content_hash(self):
        return self.canonical_job.content_hash

    @content_hash.setter
    def content_hash(self, value: str | None):
        self.canonical_job.content_hash = value

    stop: bool = False
    message_id: str | None = None
