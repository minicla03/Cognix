import logging
import os
import shutil
import traceback

from persistence.mongo.MongoDBMS import MongoConnectionManager
from persistence.mongo.NotebookRepository import MongoNotebookRepository
from rag_logic.ingestion.ingestion import IngestionFlow
from rag_logic.utils import  detect_language_from_query

#from rag_logic.memory.ChatHistory import ChatHistory

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

    def __init__(self, user_id, notebook_id, chat_id, document_path="docs", persist_dir="chroma_db"):
        """
        Initializes the Notebook with paths and user information.

        Args:
            user_id (str): The unique identifier for the user.
            document_path (str, optional): Directory where documents are stored. Defaults to "data".
            persist_dir (str, optional): Directory for the vector store persistence. Defaults to "chroma_db".
        """

        self.user_id: str = user_id
        self.notebook_id: str = notebook_id
        self.chat_id = chat_id

        self.document_path = document_path
        self.persist_dir = persist_dir

        self.force_rebuild : bool = False
        self.last_summary = None
        self.ingestion_layer = None

        try:
            self.chat_repository: IRepos.IChatRepository = ChatRepository(RedisConnectionManager.instance().client)
            self.notebook_repository: IRepos.INotebookRepository = MongoNotebookRepository(MongoConnectionManager.instance().db)
            self.ingestion_layer = IngestionFlow(self.notebook_id)

            self.ready = True
            logger.info(f"Notebook inizializzato correttamente per user {self.user_id}")
        except Exception as e:
            logger.exception(f"Errore durante l'inizializzazione del notebook per user {self.user_id}: {e}")
            self.ready = False

    def _restart(self):
        """
        Restores an existing chat session from the repository.
        """
        self.ingestion_layer = IngestionFlow(self.notebook_id)
        self.ingestion_layer.reload_vectorstore()
        self.ready = True

    def execute_rag_pipeline(self, user_query, default_language="italian", memory_ability=True, toon_format=False):
        """
        Executes the RAG pipeline for the given user query.

        Args:
            user_query (str): The user's input query.
            default_language (str, optional): Language to use if detection fails. Defaults to "italian".
            memory_ability (bool, optional): Whether the RAG pipeline is memory or not (for evaluation).
            toon_format (bool, optional): Whether the RAG pipeline is toon format (for evaluation).
        Returns:
            dict: The response from the RAG pipeline, including AI answer and metadata.
        """

        logger.info("Avvio pipeline RAG per query utente: %s", user_query)

        try:
            self.chat_repository.add_message(self.chat_id, {"type": "human", "mex": user_query})
            logger.info("User message added to chat history.")
        except Exception as e:
            logger.warning("Failed to save user message: %s", e)

        logger.info("Messaggio utente aggiunto alla cronologia.")

        language = detect_language_from_query(user_query) or default_language
        logger.info("Lingua rilevata: %s", language)

        if not self.ingestion_layer.qa_chain:
            logger.warning("Pipeline RAG non pronta")
            return {"error": "Sistema QA non pronto", "ai_response": None}

        tool = router_agent(user_query, toon_format,language)
        logger.info("Tool selezionato dal router: %s", tool)
        context = ContextFactory.create(tool)
        logger.info("Contesto creato correttamente per tool: %s", context)

        summary = None
        if memory_ability:
            if tool=="QA_pipeline":
                logger.info("Generazione del sommario delle conversazioni precedenti...")
                history_mex = self.chat_repository.get_messages(self.chat_id)
                summary = summary_agent(history_mex, toon_format, language_hint="italian")
                self.chat_repository.update_last_summary(self.chat_id, summary)
                logger.info("Sommario aggiornato nella repository.")
            else:
                summary = self.chat_repository.get_last_summary(self.chat_id)

        query={
            "user_query": user_query,
            "summary": summary,
        }

        try:
            logger.info("Esecuzione catena RAG con il contesto selezionato...")
            response = context.execute(self.ingestion_layer.qa_chain, query, language, toon_format=toon_format)
            ai_response = response.get("ai_response", "")

            self.chat_repository.add_message(self.chat_id, {"type": "system", "mex": ai_response})
            logger.info("AI response saved to chat history.")
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
            #self.chat_repository.add_documents(self.chat_id, file_path) #todo:mongo
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
            #self.chat_repository.delete_documents(self.chat_id, file_path) #todo:mongo
            print(f"[DEBUG] Documento '{file_name}' eliminato fisicamente.")
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
            return [] #self.chat_repository.get_documents(self.chat_id) #todo:mongo
        except Exception as e:
            print(f"[ERROR] Impossibile elencare i documenti: {e}")
            return []

    def _is_ready(self):
        """
        Checks if the system is ready to process queries.

        Returns:
            bool: True if ready, False otherwise.
        """

        return self.ready

    def _close(self):
        """
        Closes the chat manager and frees resources, updating chat history in the repository.
        """

        """
            Closes the chat manager, persists the last summary, and frees resources.
            """
        if not self.ready:
            logger.warning("ChatManager already closed or not initialized.")
            return

        try:
            if self.last_summary:
                try:
                    self.chat_repository.update_last_summary(self.chat_id, self.last_summary) #todo: mongo
                    logger.info(f"Last summary saved for chat {self.chat_id}")
                except Exception as e:
                    logger.warning(f"Failed to save last summary for chat {self.chat_id}: {e}")

            if self.ingestion_layer:
                try:
                    self.ingestion_layer.close()
                    logger.info(f"Ingestion layer closed for notebook {self.notebook_id}")
                except AttributeError:
                    # Se non esiste un close specifico, ignora
                    pass

        except Exception as e:
            logger.error(f"Error while closing ChatManager for chat {self.chat_id}: {e}")
        finally:
            self.ingestion_layer = None
            self.ready = False
            logger.info(f"ChatManager closed for chat {self.chat_id}")