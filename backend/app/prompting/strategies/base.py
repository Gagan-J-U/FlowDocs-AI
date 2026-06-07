from abc import ABC
from abc import abstractmethod


class BasePromptStrategy(ABC):

    @abstractmethod
    def build(
        self,
        query: str,
        chunks: list,
        figures: list | None = None
    ):
        pass