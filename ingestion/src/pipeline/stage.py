from abc import ABC
from abc import abstractmethod

from pipeline.context import PipelineContext


class PipelineStage(ABC):
    @abstractmethod
    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext: ...
