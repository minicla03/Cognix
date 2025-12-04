from typing import Optional
from pymongo import MongoClient
import os
import logging


class MongoConnectionManager:
    _instance: Optional["MongoConnectionManager"] = None
    _client: Optional[MongoClient] = None

    def __init__(self, host=None, port=None, db_name=None, username=None, password=None):
        if MongoConnectionManager._client is not None:
            return

        self.host = host or os.getenv("MONGO_HOST", "localhost")
        self.port = port or int(os.getenv("MONGO_PORT", 27017))
        self.db_name = db_name or os.getenv("MONGO_DB", "rag_system")
        self.username = username or os.getenv("MONGO_USER", None)
        self.password = password or os.getenv("MONGO_PASSWORD", None)

        if self.username and self.password:
            MongoConnectionManager._client = MongoClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password
            )
        else:
            MongoConnectionManager._client = MongoClient(host=self.host, port=self.port)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def db(self):
        if self._client is None:
            raise ConnectionError("mongo client non inizializzato.")
        return self._client[self.db_name]

    def try_connection(self):
        try:
            self._client.admin.command('ping')
            logging.info(f"Connesso a MongoDB ({self.host}:{self.port})")
            return True
        except Exception as e:
            logging.error(f"Errore di connessione a MongoDB: {e}")
            raise ConnectionError("Impossibile connettersi a MongoDB.")


