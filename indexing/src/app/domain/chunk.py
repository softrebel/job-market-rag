from pydantic import BaseModel

from app.domain.indexed_job import IndexedJobMetadata


class JobChunk(BaseModel):
    chunk_id: str

    job_id: str

    text: str

    chunk_index: int

    metadata: IndexedJobMetadata
    
