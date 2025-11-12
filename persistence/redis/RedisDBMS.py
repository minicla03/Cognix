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
        """Ritorna il client redis attivo."""
        if self._client is None:
            raise ConnectionError("redis client non inizializzato.")
        return self._client

    def try_connection(self):
        """Verifica la connessione a redis."""
        try:
            self._client.ping()
            logging.info(f"Connesso a redis ({self.host}:{self.port})")
            return True
        except redis.exceptions.ConnectionError:
            logging.error("Errore di connessione a redis.")
            raise ConnectionError("Impossibile connettersi a redis.")