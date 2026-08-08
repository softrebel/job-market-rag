from pipeline.context import PipelineContext
from pipeline.stage import PipelineStage
from services.clean_service import clean_text


class NormalizeStage(PipelineStage):
    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        context.canonical_job.title = clean_text(context.canonical_job.title)
        context.canonical_job.company = clean_text(context.canonical_job.company)
        context.canonical_job.description = clean_text(
            context.canonical_job.description
        )

        return context
