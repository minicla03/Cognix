from __future__ import annotations

import uuid
from typing import List, Dict
from threading import Lock
import ChatHistory

class Session:
    """
    Rappresenta una sessione/chat. Contiene metadata, percorso PDF, directory di persistenza
    e l'oggetto ChatHistory associato.
    """

    _registry: Dict[str, "Session"] = {}
    _registry_lock = Lock()

    def __init__(self, pdf_path: str, persist_dir: str | None = None, force_rebuild: bool = False):
        self.session_id: str = str(uuid.uuid4())
        self.pdf_path: str = pdf_path
        self.persist_dir: str = persist_dir or "memory_db"
        self.force_rebuild: bool = force_rebuild

        self.qa_chain = None
        self.ready = False

        self.history = ChatHistory(session_id=self.session_id)

        # lock per accessi concorrenti alla sessione (es. aggiungere messaggi)
        self._lock = Lock()

        # registrami nel registry
        with Session._registry_lock:
            Session._registry[self.session_id] = self

    @classmethod
    def get(cls, session_id: str) -> "Session" | None:
        """Recupera la Session dal registry (None se non esiste)."""
        return cls._registry.get(session_id)

    @classmethod
    def create(cls, pdf_path: str, persist_dir: str | None = None, force_rebuild: bool = False) -> "Session":
        """Factory per creare e registrare una nuova sessione."""
        return cls(pdf_path=pdf_path, persist_dir=persist_dir, force_rebuild=force_rebuild)

    def add_messages(self, messages):
        """Wrapper thread-safe per aggiungere messaggi alla history."""
        with self._lock:
            self.history.add_messages(messages)

    def clear_history(self):
        with self._lock:
            self.history.clear()

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "pdf_path": self.pdf_path,
            "persist_dir": self.persist_dir,
            "force_rebuild": self.force_rebuild,
            "ready": self.ready,
            "messages_count": len(self.history.get_messages()),
        }
