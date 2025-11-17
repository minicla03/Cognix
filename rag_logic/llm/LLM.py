from __future__ import annotations

import json
import logging

from langchain_core.prompt_values import StringPromptValue, ChatPromptValue
from openai import OpenAI

logger = logging.getLogger(__name__)

import threading
from typing import Any

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output
from ollama import Client
from dotenv import load_dotenv
import os

from rag_logic.utils import toon_to_json, json_to_toon


class LLM(Runnable):
    """
    Thread-safe singleton for managing a single instance of ChatOllama.

    This class exposes only one public entry point — the `chat` method — while
    fully encapsulating the underlying LLM client.

    A double-checked locking mechanism ensures safe initialization in
    multithreaded environments.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, model="llama3:latest", temperature=0.1, top_p=0.95, top_k=40):
        """
        Returns the single instance of the class (Singleton pattern).

        The method checks whether the instance already exists. If not, it uses
        a thread-safe lock to prevent the creation of multiple instances when
        accessed concurrently.

        Returns
        -------
        LLM
            The unique singleton instance of the class.
        """

        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.__initialize_client()
        return cls._instance

    def __initialize_client(self):
        """
        Privately initializes the LLM client.

        The method loads the `OLLAMA_API_KEY` environment variable,
        creates the client instance, and stores it as a private attribute.
        Keeping the client private ensures proper encapsulation and prevents
        direct external access.
        """
        load_dotenv()
        # api_key = os.getenv("OLLAMA_API_KEY")
        llama_key = os.getenv("OPEN_ROUTER")

        """self.__client = Client(
            #host="https://ollama.com",
            headers={"Authorization": f"Bearer {api_key}"}
        )"""

        self.__client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=llama_key,
        )

    def invoke(self, input: Input, config: RunnableConfig | None = None, **kwargs: Any) -> Output:
        """
        Invoca il modello con input come dizionario (e.g., {"messages": [...]}).
        Restituisce la risposta come stringa.
        """

        if isinstance(input, str):
            # Caso semplice
            messages = [{"role": "user", "content": input}]

        elif isinstance(input, StringPromptValue):
            # Prompt generato automaticamente da LangChain
            messages = [{"role": "user", "content": input.text}]

        elif isinstance(input, ChatPromptValue):
            # Prompt chat generato da LC
            messages = [{"role": m.role, "content": m.content} for m in input.messages]

        elif isinstance(input, dict):
            # Caso legacy (LLMChain con "messages")
            # Non tutti i dict hanno messages, quindi controllo
            if "messages" in input:
                messages = input["messages"]
            elif "text" in input:  # fallback langchain vecchio
                messages = [{"role": "user", "content": input["text"]}]
            else:
                raise ValueError(f"Dict input non valido: {input}")

        else:
            # Oggetto pydantic o altro serializzabile → fallback
            text = str(input)
            messages = [{"role": "user", "content": text}]

        if not messages:
            raise ValueError("Input deve contenere 'messages' oppure una stringa.")

        logger.debug(f"toon: {kwargs.get("toon_format", None)}")
        if kwargs.get("toon_format", None):
            messages = json_to_toon(messages)

        logger.info("\nTOON format: %s", messages)

        """response = self.__client.chat(
            model="gpt-oss:120b-cloud",
            messages=messages,
            options={
                "temperature": 0.1,
                "top_p": 0.9,
                "num_ctx": 4096,
                "max_tokens": 300,
                "repeat_penalty": 1.1
            },
            stream=False
        )"""

        response = self.__client.chat.completions.create(
              model="deepseek/deepseek-chat-v3.1:free",
              messages=messages
        )

        logger.info("Response: %s", response)
        if isinstance(response, str):
            response = json.loads(response)
        logger.info("Response: %s", response)

        #if kwargs.get("toon_format", None):
        #    response = toon_to_json(response)

        return response.choices[0].message.content
