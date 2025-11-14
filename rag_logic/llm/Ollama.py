import threading
from ollama import Client
from dotenv import load_dotenv
import os


class Ollama:
    """
    Thread-safe singleton for managing a single instance of ChatOllama.

    This class exposes only one public entry point — the `chat` method — while
    fully encapsulating the underlying Ollama client.

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
        Ollama
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
        Privately initializes the Ollama client.

        The method loads the `OLLAMA_API_KEY` environment variable,
        creates the client instance, and stores it as a private attribute.
        Keeping the client private ensures proper encapsulation and prevents
        direct external access.
        """
        load_dotenv()
        api_key = os.getenv("OLLAMA_API_KEY")

        self.__client = Client(
            host="https://ollama.com",
            headers={"Authorization": f"Bearer {api_key}"}
        )

    def chat(self, messages):
        """
        Executes a chat completion using the underlying Ollama client.


        Returns
        -------
        messages : list[str]
            A list of chat messages, each typically containing fields such
            as `role` and `content`.

        Returns
        -------
        str
            The textual content of the model's response.
        """
        response = self.__client.chat(
            model="gpt-oss:20b-cloud",
            messages=messages,
            options={
                "temperature": 0.1,
                "top_p": 0.9,
                "num_ctx": 4096,
                "max_tokens": 300,
                "repeat_penalty": 1.1
            },
            stream=False
        )

        return response['message']['content']

