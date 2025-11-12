from typing import List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage


class ChatHistory(BaseChatMessageHistory):

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[BaseMessage] = []

    class Config:
        arbitrary_types_allowed = True

    def add_user_message(self, message) -> None:
        """Aggiunge un messaggio dell'utente"""
        self.messages.append(message)

    def add_ai_message(self, message) -> None:
        """Aggiunge un messaggio del modello"""
        self.messages.append(message)

    def clear(self) -> None:
        """Svuota la cronologia"""
        self.messages = []