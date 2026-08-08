import redis

from dedup.base import DedupStore


class RedisDedupStore(DedupStore):
    KEY_PREFIX = "ingestion:dedup:job"

    def __init__(
        self,
        redis_client: redis.Redis,
    ):
        self.redis = redis_client

    def _key(
        self,
        content_hash: str,
    ) -> str:

        return f"{self.KEY_PREFIX}:{content_hash}"

    def mark_if_new(
        self,
        content_hash: str,
        ttl: int | None = 60 * 60 * 24 * 30,
    ) -> bool:

        key = self._key(content_hash)

        return bool(
            self.redis.set(
                key,
                "1",
                nx=True,
                ex=ttl,
            )
        )
