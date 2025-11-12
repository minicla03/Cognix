import json
import logging
import uuid
from typing import Optional, Dict, List

from persistence.IxRepository.IRepos import IChatRepository


class ChatRepository(IChatRepository):
    PREFIX = "chat_id:"
    USER_CHATS = "user_chats:"
    CHAT_MESSAGES = "chat_messages:"

    def _generate_name(self, chat_id: str) -> str:
        return f"chat_{chat_id[:8]}"

    def create_chat(self, user_id: str, document_path: str,
                    persist_dir: str, last_summary: Optional[str] = None) -> str:
        chat_id = str(uuid.uuid4())
        chat_name = self._generate_name(chat_id)

        chat_data = {
            "name_chat": chat_name,
            "document_path": document_path,
            "persist_dir": persist_dir,
            "document_list": json.dumps([]),
            "last_summary": last_summary or ""
        }

        self.redis.hset(f"{self.PREFIX}{chat_id}", mapping=chat_data)
        self.redis.sadd(f"{self.USER_CHATS}{user_id}", chat_id)

        logging.info(f"Creata chat {chat_name} ({chat_id}) per utente {user_id}")
        return chat_id

    def get_chat(self, chat_id: str) -> Optional[Dict[str, str]]:
        chat = self.redis.hgetall(f"{self.PREFIX}{chat_id}")
        if chat and "document_list" in chat:
            try:
                chat["document_list"] = json.loads(chat["document_list"])
            except json.JSONDecodeError:
                chat["document_list"] = []
        return chat or None

    def update_chat(self, chat_id: str, **kwargs) -> bool:
        """Aggiorna una chat esistente."""
        if not self.redis.exists(f"{self.PREFIX}{chat_id}"):
            raise ValueError(f"La chat {chat_id} non esiste.")
        self.redis.hset(f"{self.PREFIX}{chat_id}", mapping=kwargs)
        logging.info(f"Chat {chat_id} aggiornata con {kwargs.keys()}")
        return True

    def add_documents(self, chat_id: str, docs: List[str]) -> None:
        """Aggiunge documenti alla chat."""
        chat = self.get_chat(chat_id)
        if not chat:
            raise ValueError(f"La chat {chat_id} non esiste.")
        current_docs = chat.get("document_list", [])
        updated_docs = current_docs + docs
        self.redis.hset(f"{self.PREFIX}{chat_id}", mapping={
            "document_list": json.dumps(updated_docs)
        })
        logging.info(f"Aggiunti {len(docs)} documenti alla chat {chat_id}")

    def delete_documents(self, chat_id: str, docs: List[str]) -> None:
        chat = self.get_chat(chat_id)
        if not chat:
            raise ValueError(f"La chat {chat_id} non esiste.")
        current_docs = chat.get("document_list", [])
        current_docs.remove(docs)
        self.redis.hset(f"{self.PREFIX}{chat_id}", mapping={
            "document_list": json.dumps(current_docs)
        })
        logging.info(f"Rimossi {len(docs)} documenti alla chat {chat_id}")

    def get_documents(self, chat_id: str) -> List[str]:
        """Recupera la lista dei documenti associati a una chat."""
        chat = self.get_chat(chat_id)
        if not chat:
            raise ValueError(f"La chat {chat_id} non esiste.")
        return chat.get("document_list", [])

    def update_last_summary(self, chat_id: str, last_summary: str ) -> None:
        """"""
        chat = self.get_chat(chat_id)
        if not chat:
            raise ValueError(f"La chat {chat_id} non esiste.")

        chat["last_summary"] = last_summary
        self.redis.hset(f"{self.PREFIX}{chat_id}", mapping=chat)

    # Gestione messaggi
    def add_message(self, chat_id: str, message: str) -> None:
        """Salva un messaggio nella history."""
        self.redis.rpush(f"{self.CHAT_MESSAGES}{chat_id}", message)

    def get_messages(self, chat_id: str) -> List[str]:
        """Recupera tutti i messaggi di una chat."""
        return self.redis.lrange(f"{self.CHAT_MESSAGES}{chat_id}", 0, -1)

    def delete_messages(self, chat_id: str) -> bool:
        """Elimina tutta la history di una chat."""
        self.redis.delete(f"{self.CHAT_MESSAGES}{chat_id}")
        logging.info(f"Eliminata history messaggi per chat {chat_id}")
        return True
