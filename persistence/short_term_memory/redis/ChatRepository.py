import json
import logging
import uuid
from typing import List, Dict

from persistence.IxRepository.IRepos import IChatRepository


class ChatRepository(IChatRepository):
    """Repository for managing chat sessions and message history in Redis."""

    PREFIX = "chat_id:"
    CHAT_MESSAGES = "chat_messages:"

    MAX_MESSAGES = 10

    def __init__(self, db):
        """
        Initialize the ChatRepository with a Redis client instance.

        Args:
            db: An active Redis client connection used to persist chat data.
        """
        super().__init__(db)
        self.redis = db

    def create_chat(self, notebook_id: str) -> str:
        """
        Create a new chat session associated with a notebook.
        If a chat already exists for the notebook, returns the existing chat_id.

        Args:
            notebook_id (str): The notebook identifier.

        Returns:
            str: The chat_id for this notebook.
        """
        try:
            existing_chat_id = self.redis.get(f"{self.PREFIX}{notebook_id}")
            if existing_chat_id:
                return existing_chat_id.decode("utf-8")  # Redis returns bytes

            chat_id = str(uuid.uuid4())

            self.redis.set(f"{self.PREFIX}{notebook_id}", chat_id)
            logging.info(f"Created new chat {chat_id} for notebook {notebook_id}")

            return chat_id
        except Exception as e:
            logging.error(f"Failed to create chat for notebook {notebook_id}: {e}")
            raise


    def add_message(self, chat_id: str, message: Dict[str, str]) -> None:
        """Store a message in the chat history, keeping only the last MAX_MESSAGES messages."""
        if not isinstance(message, dict) or "type" not in message or "mex" not in message:
            raise ValueError("Invalid message format. Expected a dict with keys 'type' and 'mex'.")

        try:
            self.redis.rpush(f"{self.CHAT_MESSAGES}{chat_id}", json.dumps(message))
            self.redis.ltrim(f"{self.CHAT_MESSAGES}{chat_id}", ChatRepository.MAX_MESSAGES, -1)
        except Exception as e:
            logging.error(f"Failed to store message for chat {chat_id}: {e}")
            raise

    def get_messages(self, chat_id: str) -> List[Dict[str, str]]:
        """Retrieve all messages for a given chat session."""
        try:
            raw_messages = self.redis.lrange(f"{self.CHAT_MESSAGES}{chat_id}", 0, -1)
            messages = []
            for raw in raw_messages:
                try:
                    messages.append(json.loads(raw))
                except json.JSONDecodeError:
                    logging.warning(f"Corrupted message in chat {chat_id}: {raw}")
            return messages
        except Exception as e:
            logging.error(f"Failed to retrieve messages for chat {chat_id}: {e}")
            raise

    def reset_chat(self, chat_id: str) -> None:
        """
        Reset the chat by deleting all messages and optionally the last summary.
        """
        try:
            self.redis.delete(f"{self.CHAT_MESSAGES}{chat_id}")
            logging.info(f"Chat {chat_id} has been reset.")
        except Exception as e:
            logging.error(f"Failed to reset chat {chat_id}: {e}")
            raise

    def get_chat_id_by_notebook(self, notebook_id: str) -> str:
        """
        Retrieve the chat_id associated with a notebook.

        Args:
            notebook_id (str): The notebook identifier.

        Returns:
            str: chat_id if exists, None otherwise.
        """
        chat_id = self.redis.get(f"{self.PREFIX}{notebook_id}")
        return chat_id.decode("utf-8") if chat_id else None
