import logging

from app.messaging.redis_consumer import RedisStreamConsumer
from app.pipeline.indexer import JobIndexer


logger = logging.getLogger(__name__)


class IndexingWorker:
    def __init__(
        self,
        consumer: RedisStreamConsumer,
        indexer: JobIndexer,
    ):
        self.consumer = consumer
        self.indexer = indexer

    def run(self) -> None:

        logger.info(
            "Starting indexing worker: %s",
            self.consumer.consumer_name,
        )

        self.consumer.create_group()

        # ----------------------------------------
        # Recover stale pending messages
        # ----------------------------------------

        self._recover_pending()

        # ----------------------------------------
        # Consume new messages
        # ----------------------------------------

        for redis_message_id, message in self.consumer.consume():
            self._process_message(
                redis_message_id,
                message,
            )

    def _recover_pending(self) -> None:

        logger.info("Checking for pending messages...")

        recovered = 0

        for redis_message_id, message in self.consumer.recover_pending(
            min_idle_time=60_000,
            count=10,
        ):
            self._process_message(
                redis_message_id,
                message,
            )

            recovered += 1

        logger.info(
            "Pending recovery completed. Recovered=%d",
            recovered,
        )

    def _process_message(
        self,
        redis_message_id: str,
        message,
    ) -> None:

        try:
            logger.info(
                "Processing job=%s redis_id=%s",
                message.job.id,
                redis_message_id,
            )

            chunks_count = self.indexer.index(message.job)

            self.consumer.ack(redis_message_id)

            logger.info(
                "Successfully indexed job=%s chunks=%d redis_id=%s",
                message.job.id,
                chunks_count,
                redis_message_id,
            )

        except Exception:
            logger.exception(
                "Failed to index job=%s redis_id=%s",
                message.job.id,
                redis_message_id,
            )
