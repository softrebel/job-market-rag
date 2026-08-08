from pipeline.context import PipelineContext
from services.hash_service import HashService


class HashStage:
    def execute(
        self,
        context: PipelineContext,
    ):

        content_hash = HashService.generate(context.canonical_job)
        context.content_hash = content_hash

        return context
