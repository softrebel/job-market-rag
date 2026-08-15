import logging
import socket
import time
from collections.abc import Iterator

import redis

from app.domain.job_message import JobMessage


logger = logging.getLogger(__name__)


class RedisStreamConsumer:
    def __init__(
        self,
        client: redis.Redis,
        stream_name: str,
        group_name: str,
        consumer_name: str | None = None,
    ):
        self.client = client
        self.stream_name = stream_name
        self.group_name = group_name
        self.consumer_name = consumer_name or socket.gethostname()

    def create_group(self) -> None:
        try:
            self.client.xgroup_create(
                name=self.stream_name,
                groupname=self.group_name,
                id="0",
                mkstream=True,
            )

            logger.info(
                "Created Redis consumer group: %s",
                self.group_name,
            )

        except redis.exceptions.ResponseError as exc:
            if "BUSYGROUP" in str(exc):
                logger.debug(
                    "Redis consumer group already exists: %s",
                    self.group_name,
                )
            else:
                raise

    def consume(
        self,
        count: int = 10,
        block: int = 5000,
    ) -> Iterator[tuple[str, JobMessage]]:

        while True:
            try:
                response = self.client.xreadgroup(
                    groupname=self.group_name,
                    consumername=self.consumer_name,
                    streams={self.stream_name: ">"},
                    count=count,
                    block=block,
                )

            except (
                redis.exceptions.ConnectionError,
                redis.exceptions.TimeoutError,
            ):
                logger.exception("Redis connection error while consuming. Retrying...")

                time.sleep(2)

                continue

            for _, messages in response:
                for message_id, data in messages:
                    raw_data = data.get(b"data")

                    if raw_data is None:
                        logger.warning(
                            "Message %s has no data field",
                            message_id,
                        )
                        continue

                    if isinstance(raw_data, bytes):
                        raw_data = raw_data.decode("utf-8")

                    try:
                        message = JobMessage.model_validate_json(raw_data)

                    except Exception:
                        logger.exception(
                            "Invalid JobMessage: %s",
                            message_id,
                        )
                        continue

                    yield message_id, message

    def ack(
        self,
        message_id: str,
    ) -> None:

        self.client.xack(
            self.stream_name,
            self.group_name,
            message_id,
        )

        logger.debug(
            "ACK Redis message: %s",
            message_id,
        )

    def recover_pending(
        self,
        min_idle_time: int = 60_000,
        count: int = 10,
    ) -> Iterator[tuple[str, JobMessage]]:

        start_id = "0-0"

        while True:
            try:
                result = self.client.xautoclaim(
                    name=self.stream_name,
                    groupname=self.group_name,
                    consumername=self.consumer_name,
                    min_idle_time=min_idle_time,
                    start_id=start_id,
                    count=count,
                )

            except (
                redis.exceptions.ConnectionError,
                redis.exceptions.TimeoutError,
            ):
                logger.exception("Redis connection error during pending recovery.")

                time.sleep(2)
                continue

            next_start_id, messages, _ = result

            for message_id, data in messages:
                logger.warning(
                    "Recovered pending message: %s",
                    message_id,
                )

                message = self._parse_message(
                    message_id,
                    data,
                )

                if message is not None:
                    yield message_id, message

            if not messages:
                break

            start_id = (
                next_start_id.decode("utf-8")
                if isinstance(
                    next_start_id,
                    bytes,
                )
                else next_start_id
            )

            if start_id == "0-0":
                break

    def _parse_message(
        self,
        message_id,
        data,
    ) -> JobMessage | None:

        raw_data = data.get(b"data")

        if raw_data is None:
            logger.warning(
                "Message %s has no data field",
                message_id,
            )
            return None

        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode("utf-8")

        try:
            return JobMessage.model_validate_json(raw_data)

        except Exception:
            logger.exception(
                "Invalid JobMessage: %s",
                message_id,
            )
            return None
