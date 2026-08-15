from pydantic import BaseModel, Field


class IndexedJobMetadata(BaseModel):
    job_id: str

    title: str
    company: str
    city: str | None = None

    skills: list[str] = Field(default_factory=list)
    job_category: list[str] = Field(default_factory=list)
    salary: list[str] = Field(default_factory=list)
    gender: list[str] = Field(default_factory=list)
    employment_type: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    military_service: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)

    source: str
    url: str

    content_hash: str | None = None

    source_meta: dict[str, list[str]] = Field(default_factory=dict)
