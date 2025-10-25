import logging
import os
import shutil

from rag_logic.ingestion.ingestion import IngestionLayer
from rag_logic.qa_utils import  detect_language_from_query

from rag_logic.memory.ChatHistory import ChatHistory

from rag_logic.routing.routing_agent import router_agent
from rag_logic.routing.summary_agent import summary_agent

from rag_logic.tools.ITool import Context
from rag_logic.tools.Flashcard_pipeline import FlashcardPipeline
from rag_logic.tools.QA_pipeline import QAPipeline
from rag_logic.tools.Quiz_pipeline import QuizPipeline
from redis_db.RedisDBManager import RedisDBManager


class ChatManager:

    def __init__(self, document_path="data", persist_dir="chroma_db"):
        self.chat_id = None
        self.document_path = document_path
        self.persist_dir = persist_dir
        self.ready = False
        self.qa_chain = None
        self.force_rebuild : bool = False
        self.last_summary = None
        self.history : ChatHistory = None
        self.ingestion_layer = IngestionLayer()

        self.__initialize__(force_rebuild=self.force_rebuild)

    def __initialize__(self, force_rebuild):
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
            chat_id=RedisDBManager.instance().create_chat()
            self.chat_id = chat_id
            self.qa_chain = self.ingestion_layer.qa_chain
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
            path_doc, path_vectorstore, last_summary = RedisDBManager.instance().retrieve_chat(user_id, id_chat)
            self.last_summary = last_summary
            self.document_path = path_doc
            self.persist_dir = path_vectorstore
            self.force_rebuild = False
            self.qa_chain = self.ingestion_layer.qa_chain #todo: da controllare
            self.ready = True
        except Exception as e:
            logging.exception("QA restart error\n", e.with_traceback())
            self.qa_chain = None
            self.ready = False
            self.history = None

    def execute_rag_pipeline(self, user_query, default_language="italian"):

        self.history.add_user_message(user_query)
        language = detect_language_from_query(user_query) or default_language

        if not self.qa_chain:
            return "Sistema QA non pronto", []

        tool = router_agent(user_query, language)

        context = None #todo: prevedi classe con etichette
        if tool == "QA_TOOL": context = Context(QAPipeline())
        elif tool == "FLASHCARD_TOOL": context = Context(FlashcardPipeline())
        elif tool == "QUIZ_TOOL": context = Context(QuizPipeline())

        summary = None
        if self.history:
            summary = summary_agent(self.history.get_messages(),language_hint="italian")

        query={
            "user_query": user_query,
            "summary": summary,
        }

        try:
            #todo: save the ai mex
            return context.execute(self.qa_chain, query, language)
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
            #todo: sync db
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
            # todo: sync db
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
            # todo: from db ??
            return sorted([
                f for f in os.listdir(self.document_path)
                if f.lower().endswith(".pdf") and os.path.isfile(os.path.join(self.document_path, f))
            ])
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
            RedisDBManager.instance().save_chat(
                self.chat_id,
                self.history.get_messages(),
                self.last_summary
            )
            if RedisDBManager.instance().delete_message_history(self.chat_id):
                self.history = None
        self.qa_chain = None
        self.ready = False
