import logging
import os
import shutil

from rag_logic.ingestion.ingestion import IngestionFlow
from rag_logic.qa_utils import  detect_language_from_query

from rag_logic.memory.ChatHistory import ChatHistory

from rag_logic.routing.routing_agent import router_agent
from rag_logic.routing.summary_agent import summary_agent

from rag_logic.tools.ITool import ContextFactory
from redis_db.RedisDBMS import IChatRepository, RedisConnectionManager


class ChatManager:

    def __init__(self, user_id, document_path="data", persist_dir="chroma_db"):
        self.chat_id = None
        self.document_path = document_path
        self.persist_dir = persist_dir
        self.ready = False
        self.force_rebuild : bool = False
        self.last_summary = None
        self.history : ChatHistory = None
        self.ingestion_layer = IngestionFlow()
        self.chat_repository : IChatRepository() = None

        self.__initialize__(user_id)

    def __initialize__(self, user_id):
        """
        Inizializza il sistema QA, creando o caricando il vector store.
        Args:
            force_rebuild (bool): Se True, ricrea il sistema QA anche se esiste già.
        Returns:
            None
        Raises:
            Exception: Se si verifica un errore durante l'inizializzazione.
        """
        try:
            self.chat_repository = IChatRepository(RedisConnectionManager.client)
            chat_id=  self.chat_repository.create_chat(user_id, self.document_path, self.persist_dir)
            self.chat_id = chat_id
            self.ready = True
            self.history = ChatHistory(session_id=chat_id)
        except Exception as e:
            logging.exception("QA initialization error\n", e.with_traceback())
            self.qa_chain = None
            self.ready = False
            self.history = None

    def __restart__(self, user_id, id_chat):
        """..."""
        try:
            path_doc, path_vectorstore, last_summary =  self.chat_repository.retrieve_chat(user_id, id_chat)
            self.last_summary = last_summary
            self.document_path = path_doc
            self.persist_dir = path_vectorstore
            self.force_rebuild = False
            self.ready = True
        except Exception as e:
            logging.exception("QA restart error\n", e.with_traceback())
            self.qa_chain = None
            self.ready = False
            self.history = None

    def execute_rag_pipeline(self, user_query, default_language="italian"):

        self.history.add_user_message(user_query)
        language = detect_language_from_query(user_query) or default_language

        self.history.add_user_message(user_query)

        if not self.qa_chain:
            return "Sistema QA non pronto", []

        tool = router_agent(user_query, language)
        logging.info("[INFO]",tool)
        context = ContextFactory.create(tool)

        summary = None
        if self.history and tool=="QA_pipeline":
            summary = summary_agent(self.history.get_messages(),language_hint="italian")
            self.chat_repository.update_last_summary(summary)

        query={
            "user_query": user_query,
            "summary": summary,
        }

        try:
           response = context.execute(self.ingestion_layer.qa_chain, query, language)
           self.history.add_ai_message(response["ai_response"]) if response["type"] == "QA_TOOL" else None
           return response
        except BaseException as be:
            raise be.with_traceback()

    def add_document(self, file_path):
        """
        Aggiunge un nuovo documento PDF al vectorstore esistente.
        """
        print(f"[DEBUG] Aggiunta documento: {file_path}")

        dest_path = os.path.join(self.document_path, os.path.basename(file_path))
        if not os.path.exists(dest_path):
            shutil.copy(file_path, dest_path)
        print(f"[DEBUG] Documento copiato in: {dest_path}")

        try:
            self.ingestion_layer.add_document_to_vectorstore(file_path)
            self.chat_repository.add_documents(self.chat_id, file_path)
            print(f"[DEBUG] Documento aggiunto al vectorstore con successo")
        except Exception as e:
            print(f"[ERROR] Errore durante l'aggiunta al vectorstore: {e}")
            return

    def delete_document(self, file_name):
        """
        Elimina un documento PDF dalla directory e i suoi chunk dal vectorstore.

        Args:
            file_name (str): Il nome del file (es. "Android.pdf") da eliminare.
        """
        file_path = os.path.join(self.document_path, file_name)

        if not os.path.exists(file_path):
            print(f"[ERROR] Il documento '{file_name}' non esiste nella directory dei PDF.")
            return False

        print(f"[DEBUG] Eliminazione documento: {file_path}")
        try:
            self.ingestion_layer.delete_document_from_vectorstore(file_name)
            os.remove(file_path)
            self.chat_repository.delete_documents(self.chat_id, file_path)
            print("[DEBUG] Documento '{file_name}' eliminato fisicamente.")
            return True
        except Exception as e:
            print(f"[ERROR] Errore durante l'eliminazione del documento: {e}")
            return False

    def list_documents(self):
        """
        Restituisce una lista dei documenti attualmente presenti nella directory `document_path`.
        """
        try:
            return  self.chat_repository.get_documents(self.chat_id)
        except Exception as e:
            print(f"[ERROR] Impossibile elencare i documenti: {e}")
            return []

    def is_ready(self):
        """
        Verifica se il sistema è pronto per rispondere alle domande.
        """
        return self.ready

    def __close__(self):
        """Chiude il sistema e libera le risorse."""
        if self.history:
            self.chat_repository.update_chat(
                self.chat_id,
                self.history.get_messages()
            )
        self.history = None
        self.qa_chain = None
        self.ready = False