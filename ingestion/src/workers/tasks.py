from workers.celery import celery


@celery.task
def crawl_jobs():

    from sources.crawler.jobinja import JobinjaCrawler
    from pipeline.pipeline import IngestionPipeline

    crawler = JobinjaCrawler()

    pipeline = IngestionPipeline(crawler.repository)

    for job in crawler.crawl():
        pipeline.process(job)
