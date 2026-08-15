import logging

import redis

from app.config.settings import settings
from app.chunking.job_chunker import JobChunker
from app.messaging.redis_consumer import RedisStreamConsumer
from app.normalization.job_metadata import JobMetadataNormalizer


logging.basicConfig(
    level=logging.DEBUG,
)


def main():

    client = redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=False,
    )

    consumer = RedisStreamConsumer(
        client=client,
        stream_name=settings.REDIS_STREAM_NAME,
        group_name="debug-group",
        consumer_name="debug",
    )

    consumer.create_group()

    normalizer = JobMetadataNormalizer()

    chunker = JobChunker(
        normalizer=normalizer,
    )

    print("Waiting for job...")

    for redis_id, message in consumer.consume(
        count=1,
        block=5000,
    ):
        print("\nRedis ID:")
        print(redis_id)

        print("\nJob:")
        print(message.job.model_dump_json(indent=2))

        metadata = normalizer.normalize(message.job)

        print("\nNormalized metadata:")
        print(metadata.model_dump_json(indent=2))

        chunks = chunker.chunk(message.job)

        print("\nChunks:")

        for chunk in chunks:
            print("=" * 80)
            print("ID:", chunk.chunk_id)
            print(chunk.text)

        break


if __name__ == "__main__":
    main()
