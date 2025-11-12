from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from persistence.model.Flashcard import Flashcard
from persistence.model.Quiz import Quiz


class BaseRepository(ABC):
    def __init__(self, db):
        self.db = db


class IUserRepository(BaseRepository):

    @abstractmethod
    def create_user(self, name: str, password: str, email: str) -> str:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, str]]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict[str, str]]:
        pass

    @abstractmethod
    def get_user_notebooks(self, user_id: str) -> List[Dict]:
        pass

class IChatRepository(BaseRepository):

    @abstractmethod
    def create_chat(self, user_id: str, document_path: str,
                    persist_dir: str, last_summary: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def get_chat(self, chat_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def update_chat(self, chat_id: str, **kwargs) -> bool:
        pass

    @abstractmethod
    def add_documents(self, chat_id: str, docs: List[str]) -> None:
        pass

    @abstractmethod
    def delete_documents(self, chat_id: str, docs: List[str]) -> None:
        pass

    @abstractmethod
    def get_documents(self, chat_id: str) -> List[str]:
        pass

    @abstractmethod
    def update_last_summary(self, chat_id: str, last_summary: str) -> None:
        pass

class INotebookRepository(BaseRepository):

    @abstractmethod
    def create_notebook(self, notebook) -> str:
        pass

    @abstractmethod
    def get_notebook_by_id(self, notebook_id: str) -> Optional[Dict]:
        pass

    def get_notebook_by_user(self, notebook_id: str) -> Optional[Dict]:
        pass

    def delete_notebook(self, notebook_id: str) -> bool:
        pass

    @abstractmethod
    def update_chat_metadata(self, notebook_id: str, last_chat_id: str, summary: str) -> None:
        pass

    @abstractmethod
    def update_notebook(self, notebook):
        pass

class IFlashcardRepository(BaseRepository):
    @abstractmethod
    def create_flashcard(self, flashcard) -> str:
        pass

    @abstractmethod
    def get_flashcard_by_user(self, user_id: str) -> List[Flashcard]:
        pass

    @abstractmethod
    def get_flashcard_by_notebook(self, notebook_id: str) -> List[Flashcard]:
        pass

    @abstractmethod
    def delete_flashcard(self, flashcard_id: str) -> bool:
        pass


class IQuizRepository(BaseRepository):
    @abstractmethod
    def create_quiz(self, quiz) -> str:
        pass

    @abstractmethod
    def get_quiz_by_user(self, user_id: str) -> List[Quiz]:
        pass

    @abstractmethod
    def get_quiz_by_notebook(self, notebook_id: str) -> List[Quiz]:
        pass

    @abstractmethod
    def delete_quiz(self, quiz_id: str) -> bool:
        pass
