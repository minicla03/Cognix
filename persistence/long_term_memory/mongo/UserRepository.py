import logging
from typing import Optional, Dict, List
from bson import ObjectId

from persistence.IxRepository import IRepos


class MongoUserRepository(IRepos.IUserRepository):

    USERS_COLLECTION = "users"
    NOTEBOOKS_COLLECTION = "notebooks"

    def __init__(self, db):
        super().__init__(db)

    def create_user(self, name: str, password: str, email: str) -> str:
        user_doc = {
            "_id": ObjectId(),
            "username": name,
            "email": email,
            "password": password,
            "created_at": None,
            "notebooks": []
        }
        result = self.db[self.USERS_COLLECTION].insert_one(user_doc)
        user_id = str(result.inserted_id)
        logging.info(f"Creato utente {name} ({user_id})")
        return user_id

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, str]]:
        user = self.db[self.USERS_COLLECTION].find_one({"_id": ObjectId(user_id)})
        if not user:
            return None

        user_dict = {k: v for k, v in user.items() if k != "_id"}
        user_dict["id"] = str(user["_id"])
        return user_dict

    def get_user_by_email(self, email: str) -> Optional[Dict[str, str]]:
        user = self.db[self.USERS_COLLECTION].find_one({"email": email})

        if not user:
            return None

        user_dict = {k: v for k, v in user.items() if k != "_id"}
        user_dict["id"] = str(user["_id"])
        return user_dict

    def get_user_notebooks(self, user_id: str) -> List[Dict]:
        user = self.db[self.USERS_COLLECTION].find_one({"_id": ObjectId(user_id)})

        if not user or "notebooks" not in user:
            return []

        return [{"id": str(nb["_id"]), "name": nb.get("name", "")} for nb in user]
