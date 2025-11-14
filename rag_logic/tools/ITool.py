from __future__ import annotations

import importlib
from abc import abstractmethod, ABC
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
            tool_name = tool_name.lower()
            tool_map = {
                "qa_tool": ("rag_logic.tools.QATool", "QATool"),
                "flashcard_tool": ("rag_logic.tools.FlashcardTool", "FlashcardTool"),
                "quiz_tool": ("rag_logic.tools.QuizTool", "QuizTool"),
            }

            if tool_name not in tool_map:
                raise ValueError(f"Tool '{tool_name}' non riconosciuto")

            module_name, class_name = tool_map[tool_name]
            module = importlib.import_module(module_name)
            tool_class = getattr(module, class_name)
            return Context(tool_class())
        except KeyError:
            return None


class IToolStrategy(ABC):

    @abstractmethod
    def execute(self, qa_chain, query: dict, language: str = "italian", toon_format: bool = False) -> dict:
        pass
