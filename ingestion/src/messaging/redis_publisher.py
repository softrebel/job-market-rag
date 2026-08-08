import redis

from domain.job_message import JobMessage
from messaging.publisher import BasePublisher


class RedisStreamPublisher(BasePublisher):
    STREAM_NAME = "jobs.ingested"

    def __init__(
        self,
        client: redis.Redis,
    ):
        self.client = client

    def publish(
        self,
        message: JobMessage,
    ) -> str:

        message_id = self.client.xadd(
            self.STREAM_NAME, {"data": message.model_dump_json()}
        )

        return message_id
