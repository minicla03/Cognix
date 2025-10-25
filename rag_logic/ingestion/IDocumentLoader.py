from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document

class DocumentLoaderStrategy(ABC):
    @abstractmethod
    def load(self, file_path: str) -> List[Document]:
        """Carica e restituisce una lista di Document da un file o sorgente."""
        pass
