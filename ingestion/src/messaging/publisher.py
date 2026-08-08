from abc import ABC
from abc import abstractmethod

from domain.job_message import JobMessage


class BasePublisher(ABC):
    @abstractmethod
    def publish(
        self,
        message: JobMessage,
    ) -> str: ...
