from typing import Optional, Dict

from persistence.IxRepository.IRepos import IQuizRepository


class MongoQuizRepository(IQuizRepository):

    def __init__(self, db):
        super().__init__(db)

    def delete_quiz(self, quiz_id: str) -> bool:
        pass

    def create_quiz(self, quiz) -> str:
        pass

    def get_quiz_by_user(self, user_id: str) -> Optional[Dict]:
        pass

    def get_quiz_by_notebook(self, notebook_id: str) -> Optional[Dict]:
        pass