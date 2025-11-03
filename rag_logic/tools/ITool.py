from __future__ import annotations
from abc import ABC, abstractmethod
from langchain.tools import BaseTool

class Context:

    def __init__(self, strategy: IToolStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> IToolStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: IToolStrategy) -> None:
        self._strategy = strategy

    def execute(self, *args, **kwargs) -> dict:
        return self._strategy.execute(*args, **kwargs)

class ContextFactory:
    @staticmethod
    def create(tool_name: str) -> Context | None:
        try:
            PipelineClass = globals()[tool_name.replace("_TOOL", "Pipeline")]
            return Context(PipelineClass())
        except KeyError:
            return None

class IToolStrategy(ABC, BaseTool):

    @abstractmethod
    def execute(self, qa_chain, query: dict, language: str = "italian") -> dict:
        pass

