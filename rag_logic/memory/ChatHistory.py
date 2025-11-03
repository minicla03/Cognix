from abc import ABC
from typing import List
from pydantic import BaseModel, Field
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage

from redis_db.ChatRepository import ChatRepository


class ChatHistory(BaseChatMessageHistory, BaseModel, ABC):

    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id
        self.messages: List[BaseMessage] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    def add_user_message(self, message) -> None:
        """Aggiunge un messaggio dell'utente"""
        self.messages.append(message)

    def add_ai_message(self, message) -> None:
        """Aggiunge un messaggio del modello"""
        self.messages.append(message)

    def clear_history(self) -> None:
        """Svuota la cronologia"""
        self.messages = []