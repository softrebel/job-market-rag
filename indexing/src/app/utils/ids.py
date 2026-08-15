import hashlib


def make_chunk_id(
    job_id: str,
    chunk_index: int,
    content_hash: str | None = None,
) -> str:
    value = f"{job_id}:{chunk_index}:{content_hash or ''}"

    return hashlib.sha256(value.encode("utf-8")).hexdigest()
