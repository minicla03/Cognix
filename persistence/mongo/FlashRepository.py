from typing import Optional, Dict

from persistence.IxRepository.IRepos import IFlashcardRepository


class MongoFlashRepository(IFlashcardRepository):

    def __init__(self, db):
        super().__init__(db)

    def delete_flashcard(self, flashcard_id: str) -> bool:
        pass

    def create_flashcard(self, flashcard) -> str:
        pass

    def get_flashcard_by_user(self, user_id: str) -> Optional[Dict]:
        pass

    def get_flashcard_by_notebook(self, notebook_id: str) -> Optional[Dict]:
        pass