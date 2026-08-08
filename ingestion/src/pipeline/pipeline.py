from pipeline.context import PipelineContext
from pipeline.stage import PipelineStage
from domain.canonical_job import CanonicalJob


class IngestionPipeline:
    def __init__(
        self,
        stages: list[PipelineStage],
    ):

        self.stages = stages

    def run(
        self,
        canonical_job: CanonicalJob,
    ) -> PipelineContext:

        context = PipelineContext(canonical_job=canonical_job)

        for stage in self.stages:
            context = stage.execute(context)

            if context.stop:
                break

        return context
