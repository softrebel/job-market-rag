from domain.job_message import JobMessage
from pipeline.context import PipelineContext
from pipeline.stage import PipelineStage
from messaging.publisher import BasePublisher


class PublishStage(PipelineStage):
    def __init__(
        self,
        publisher: BasePublisher,
    ):
        self.publisher = publisher

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        message = JobMessage(job=context.canonical_job)

        redis_id = self.publisher.publish(message)

        context.message_id = redis_id

        return context
