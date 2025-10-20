from __future__ import annotations
from abc import ABC, abstractmethod

class Context:

    def __init__(self, strategy: IToolStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> IToolStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: IToolStrategy) -> None:
        self._strategy = strategy

    def execute(self, *args, **kwargs) -> None:
        return self._strategy.execute(*args, **kwargs)

class IToolStrategy(ABC):

    @abstractmethod
    def execute(self, qa_chain, query: str, language: str = "italian"):
        pass

