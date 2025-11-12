import logging
import os
import shutil
import traceback

from rag_logic.ingestion.ingestion import IngestionFlow
from rag_logic.qa_utils import  detect_language_from_query

from rag_logic.memory.ChatHistory import ChatHistory

from rag_logic.agents.routing_agent import router_agent
from rag_logic.agents.summarizer_agent import summary_agent

from rag_logic.tools.ITool import ContextFactory

from persistence.IxRepository import IRepos
from persistence.redis.RedisDBMS import RedisConnectionManager
from persistence.redis.ChatRepository import ChatRepository

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

class ChatManager:
    """
       Manages a chat session for a user, including document management,
       chat history, and execution of the RAG (Retrieval-Augmented Generation) pipeline.
    """

    def __init__(self, user_id, document_path="docs", persist_dir="chroma_db"):
        """
        Initializes the Notebook with paths and user information.

        Args:
            user_id (str): The unique identifier for the user.
            document_path (str, optional): Directory where documents are stored. Defaults to "data".
            persist_dir (str, optional): Directory for the vector store persistence. Defaults to "chroma_db".
        """

        self.user_id: str = user_id
        self.chat_id = None
        self.document_path = document_path
        self.persist_dir = persist_dir
        self.ready = False
        self.force_rebuild : bool = False
        self.last_summary = None

        self.ingestion_layer = IngestionFlow()
        self.chat_repository: IRepos.IChatRepository = ChatRepository(RedisConnectionManager.client) #todo: redis
        #self.history = None #todo: rimuovere fare tutto tramite redis

        self.__initialize__()

    def __initialize__(self):
        """
       Creates a new chat session in the repository and initializes chat history.
       Sets the manager as ready if successful.
       """

        try:
            self.chat_id = self.chat_repository.create_chat(
                self.user_id, self.document_path, self.persist_dir
            )
            self.history = ChatHistory(session_id=self.chat_id)
            self.ready = True
            logger.info(f"Notebook inizializzato correttamente per user {self.user_id}")
        except Exception as e:
            logger.exception("Errore durante l'inizializzazione della chat")
            self.ready = False

    def __restart__(self, user_id, chat_id):
        """
        Restores an existing chat session from the repository.


        """
        # todo: da definire



    def execute_rag_pipeline(self, user_query, default_language="italian", memory_ability=True):
        """
        Executes the RAG pipeline for the given user query.

        Args:
            user_query (str): The user's input query.
            default_language (str, optional): Language to use if detection fails. Defaults to "italian".
            memory_ability (bool, optional): Whether the RAG pipeline is memory or not (for evaluation).
        Returns:
            dict: The response from the RAG pipeline, including AI answer and metadata.
        """

        logger.info("Avvio pipeline RAG per query utente: %s", user_query)

        self.history.add_user_message(user_query) #todo:dict type-mex
        logger.info("Messaggio utente aggiunto alla cronologia.")

        language = detect_language_from_query(user_query) or default_language
        logger.info("Lingua rilevata: %s", language)

        if not self.ingestion_layer.qa_chain:
            logger.warning("Pipeline RAG non pronta")
            return {"error": "Sistema QA non pronto", "ai_response": None}

        tool = router_agent(user_query, language)
        logger.info("Tool selezionato dal router: %s", tool)
        context = ContextFactory.create(tool)
        logger.info("Contesto creato correttamente per tool: %s", context)

        summary = None
        if memory_ability:
            if self.history and tool=="QA_pipeline":
                logger.info("Generazione del sommario delle conversazioni precedenti...")
                summary = summary_agent(self.history.get_messages(),language_hint="italian")
                self.chat_repository.update_last_summary(summary)
                logger.info("Sommario aggiornato nella repository.")

        query={
            "user_query": user_query,
            "summary": summary,
        }

        try:
            logger.info("Esecuzione catena RAG con il contesto selezionato...")
            response = context.execute(self.ingestion_layer.qa_chain, query, language)
            self.history.add_ai_message(response["ai_response"]) if response["type"] == "QA_TOOL" else None

            logger.info("Esecuzione completata con successo.")
            return response
        except Exception as e:
            tb_str = traceback.format_exc()
            logger.error("Errore durante l'esecuzione della pipeline RAG: %s", str(e))
            logger.debug("Traceback completo:\n%s", tb_str)
            return {
                "error": f"Errore interno: {str(e)}",
                "traceback": tb_str,
                "ai_response": None
            }

    def add_document(self, file_path):
        """
        Adds a new document to the vector store and repository.

        Args:
            file_path (str): Path to the document to add.
        """

        os.makedirs(self.document_path, exist_ok=True)

        print(f"[DEBUG] Aggiunta documento: {file_path}")

        dest_path = os.path.join(self.document_path, os.path.basename(file_path))
        if not os.path.exists(dest_path):
            shutil.copy(file_path, dest_path)
        print(f"[DEBUG] Documento copiato in: {dest_path}")

        try:
            self.ingestion_layer.add_document_to_vectorstore(file_path)
            self.chat_repository.add_documents(self.chat_id, file_path) #todo:mongo
            print(f"[DEBUG] Documento aggiunto al vectorstore con successo")
        except Exception as e:
            print(f"[ERROR] Errore durante l'aggiunta al vectorstore: {e}")
            return

    def delete_document(self, file_name):
        """
        Deletes a document from the directory and its chunks from the vector store.

        Args:
            file_name (str): Name of the file to delete (e.g., "Android.pdf").

        Returns:
            bool: True if deletion was successful, False otherwise.
        """

        file_path = os.path.join(self.document_path, file_name)

        if not os.path.exists(file_path):
            print(f"[ERROR] Il documento '{file_name}' non esiste nella directory dei PDF.")
            return False

        print(f"[DEBUG] Eliminazione documento: {file_path}")
        try:
            self.ingestion_layer.delete_document_from_vectorstore(file_name)
            os.remove(file_path)
            self.chat_repository.delete_documents(self.chat_id, file_path) #todo:mongo
            print("[DEBUG] Documento '{file_name}' eliminato fisicamente.")
            return True
        except Exception as e:
            print(f"[ERROR] Errore durante l'eliminazione del documento: {e}")
            return False

    def list_documents(self):
        """
        Returns a list of documents currently present in the chat session.

        Returns:
            list[str]: List of document filenames.
        """

        try:
            return self.chat_repository.get_documents(self.chat_id) #todo:mongo
        except Exception as e:
            print(f"[ERROR] Impossibile elencare i documenti: {e}")
            return []

    def is_ready(self):
        """
        Checks if the system is ready to process queries.

        Returns:
            bool: True if ready, False otherwise.
        """

        return self.ready

    def __close__(self):
        """
        Closes the chat manager and frees resources, updating chat history in the repository.
        """
        if self.history:
            self.chat_repository.update_chat(
                self.chat_id,
                self.history.get_messages() #todo:mongodb
            )
        self.history = None
        self.ingestion_layer = None
        self.ready = False