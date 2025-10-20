# rag_logic/memory/chat_history.py

from typing import List
from threading import Lock
from pydantic import BaseModel, Field
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage


class ChatHistory(BaseChatMessageHistory, BaseModel):

    session_id: str
    messages: List[BaseMessage] = Field(default_factory=list)
    _lock: Lock = Field(default_factory=Lock, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    # === API standard LangChain ===
    def add_user_message(self, message: str) -> None:
        """Aggiunge un messaggio dell'utente"""
        with self._lock:
            self.messages.append(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        """Aggiunge un messaggio del modello"""
        with self._lock:
            self.messages.append(AIMessage(content=message))

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Aggiunge una lista di messaggi"""
        with self._lock:
            self.messages.extend(messages)

    def get_messages(self) -> List[BaseMessage]:
        """Restituisce una copia dei messaggi"""
        with self._lock:
            return list(self.messages)

    def clear(self) -> None:
        """Svuota la cronologia"""
        with self._lock:
            self.messages = []
