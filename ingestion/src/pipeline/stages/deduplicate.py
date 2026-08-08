from dedup.base import DedupStore

from pipeline.context import PipelineContext


class DeduplicateStage:
    def __init__(
        self,
        store: DedupStore,
    ):
        self.store = store

    def execute(
        self,
        context: PipelineContext,
    ):

        is_new = self.store.mark_if_new(context.content_hash)

        # TODO: Uncomment after debug ends.
        # if not is_new:
        #     context.stop = True

        return context
