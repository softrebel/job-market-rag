import redis

from app.messaging.redis_consumer import RedisStreamConsumer


from pathlib import Path

from app.domain.job_message import JobMessage


def test_parse_real_job_message():

    path = Path("tests/fixtures/job_message.json")

    message = JobMessage.model_validate_json(path.read_text(encoding="utf-8"))

    assert message.job.id == "1"
    assert message.job.source == "jobinja"


def test_redis_stream():

    client = redis.Redis(
        host="localhost",
        port=6379,
        db=15,
        decode_responses=False,
    )

    consumer = RedisStreamConsumer(
        client=client,
        stream_name="test.jobs.ingested",
        group_name="test-indexers",
        consumer_name="test-consumer",
    )

    consumer.create_group()

    # بعداً یک JobMessage واقعی publish می‌کنیم
