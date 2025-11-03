from __future__ import annotations

import os
from abc import abstractmethod
from typing import Optional, Dict, List

import redis
import logging


import os
import redis
import logging
from typing import Optional

class RedisConnectionManager:

    _instance: Optional["RedisConnectionManager"] = None
    _client: Optional[redis.Redis] = None

    def __init__(self, host=None, port=None, password=None, db=None):

        if RedisConnectionManager._client is not None:
            return

        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.password = password or os.getenv("REDIS_PASSWORD", None)
        self.db = db or int(os.getenv("REDIS_DB", 0))

        RedisConnectionManager._client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            decode_responses=True
        )

    @classmethod
    def instance(cls):
        """Ritorna un'unica istanza del Connection Manager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def client(self) -> redis.Redis:
        """Ritorna il client Redis attivo."""
        if self._client is None:
            raise ConnectionError("Redis client non inizializzato.")
        return self._client

    def try_connection(self):
        """Verifica la connessione a Redis."""
        try:
            self._client.ping()
            logging.info(f"Connesso a Redis ({self.host}:{self.port})")
            return True
        except redis.exceptions.ConnectionError:
            logging.error("Errore di connessione a Redis.")
            raise ConnectionError("Impossibile connettersi a Redis.")


class BaseRepository:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

class IUserRepository(BaseRepository):

    @abstractmethod
    def create_user(self, name: str, password: str, email: str) -> str:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[Dict[str, str]]:
        pass

    @abstractmethod
    def get_user_chats(self, user_id: str) -> List[str]:
        pass

class IChatRepository(BaseRepository):

    @abstractmethod
    def create_chat(self, user_id: str, document_path: str,
                    persist_dir: str, last_summary: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def get_chat(self, chat_id: str) -> Optional[Dict[str, str]]:
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
    def update_last_summary(self, chat_id: str, last_summary: str ) -> None:
        pass