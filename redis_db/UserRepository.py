import logging
import uuid
from typing import Optional, Dict, List

from redis_db.RedisDBM import BaseRepository


class UserRepository(BaseRepository):
    PREFIX = "user_id:"
    USER_CHATS = "user_chats:"

    def create_user(self, name: str, password: str, email: str) -> str:
        user_id = str(uuid.uuid4())
        self.redis.hset(f"{self.PREFIX}{user_id}", mapping={
            "username": name,
            "email": email,
            "password": password
        })
        logging.info(f"Creato utente {name} ({user_id})")
        return user_id

    def get_user(self, user_id: str) -> Optional[Dict[str, str]]:
        user = self.redis.hgetall(f"{self.PREFIX}{user_id}")
        return user or None

    def get_user_chats(self, user_id: str) -> List[str]:
        """Ritorna tutti gli ID chat di un utente."""
        return list(self.redis.smembers(f"{self.USER_CHATS}{user_id}"))

