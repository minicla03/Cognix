from __future__ import annotations

import os
import redis
import logging


class RedisConnectionManager:
    
    def __init__(self, host=None, port=None, password=None, db=None):
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.password = password or os.getenv("REDIS_PASSWORD", None)
        self.db = db or int(os.getenv("REDIS_DB", 0))

        self._client = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                decode_responses=True
            )
            try:
                self._client.ping()
                logging.info(f"Connesso a Redis ({self.host}:{self.port})")
            except redis.exceptions.ConnectionError as e:
                logging.error("Errore di connessione a Redis.")
                raise ConnectionError("Impossibile connettersi a Redis")
        return self._client

class BaseRepository:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client