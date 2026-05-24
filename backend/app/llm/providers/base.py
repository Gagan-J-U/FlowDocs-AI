from abc import ABC
from abc import abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(

        self,

        prompt: str,

        temperature: float = 0.2
    ) -> str:

        pass

    @abstractmethod
    def stream(

        self,

        prompt: str,

        temperature: float = 0.2
    ):

        pass