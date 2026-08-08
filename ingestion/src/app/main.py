from sqlalchemy import text
from pathlib import Path

from config.logging import logger

from config.settings import settings

from pipeline.pipeline import IngestionPipeline
from pipeline.stages import PublishStage, DeduplicateStage, HashStage, NormalizeStage
from dedup.redis_store import RedisDedupStore
import redis
from messaging.redis_publisher import RedisStreamPublisher
from database.session import get_db
from extractors.base import BaseExtractor
from extractors.crawlers.jobinja import JobinjaCrawler
from extractors.postgres_extractor.extractor import PostgresExtractor
from repositories.job_repository import JobRepository


def main():

    logger.info("Starting %s", settings.APP_NAME)

    # db = SessionLocal()
    # raw = RawJob(
    #     title="Python Backend Developer",
    #     company="Snapp",
    #     description="Develop APIs with FastAPI and PostgreSQL.",
    #     city="Tehran",
    #     source="manual",
    #     source_url="https://example.com/job/1",
    # )

    try:
        redis_client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

        messages = redis_client.xrange("jobs.ingested", "-", "+")

        for message_id, data in messages:
            print("ID:", message_id)
            print("DATA:", data)
            print("-" * 50)

        # raise

        with get_db() as db:
            db.execute(text("SELECT 1"))

            logger.info("Database Connected")

            # jobs = repo.fetch_jobs_batch(0, 10)
            # print(jobs)

            redis_publisher = RedisStreamPublisher(client=redis_client)
            pipeline = IngestionPipeline(
                stages=[
                    NormalizeStage(),
                    HashStage(),
                    DeduplicateStage(RedisDedupStore(redis_client)),
                    PublishStage(publisher=redis_publisher),
                ]
            )
            job_repo = JobRepository(db=db)
            extractors: list[BaseExtractor] = [
                PostgresExtractor(job_repo),
                JobinjaCrawler(
                    username=settings.JOBINJA_USERNAME,
                    password=settings.JOBINJA_PASSWORD,
                    data_path=Path(settings.DATA_PATH),
                ),
            ]
            enabled_extractors = [
                ext for ext in extractors if ext.source_name in settings.ENABLED_SOURCES
            ]
            for extractor in enabled_extractors:
                logger.info("Running %s", extractor.source_name)

                # TODO: Debug Just 3 items for each extractor, then remove it.
                cnt = 0
                for job in extractor.iter_raw_documents():
                    pipeline.run(job)
                    cnt += 1
                    if cnt >= 3:
                        break

        # i = 0
        # for item in crawler.discover_urls():
        #     if i >= 10:
        #         break

        #     print(item)
        #     i += 1

        # content_hash = HashService.generate(raw)
        # job = RawJobMapper.raw_to_job(raw)
        # model = JobModelMapper.job_to_model(job, content_hash)
        # repo = JobRepository(db)

        # repo.create(
        #     Job(
        #         title="Python Developer",
        #         company="Snapp",
        #         description="FastAPI + Docker",
        #         city="Tehran",
        #         source="manual",
        #         source_url="https://example.com",
        #     )
        # )
        # print(raw)
        # print()

        # print(job)
        # print()

        # print(model)
        # print()

        # print(content_hash)

        # repo.save(model)

        # print("Saved successfully")

    finally:
        db.close()


if __name__ == "__main__":
    main()
