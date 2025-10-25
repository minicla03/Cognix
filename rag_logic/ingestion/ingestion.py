"""
Questo modulo gestisce l'ingestione dei dati da documenti PDF che
verranno utilizzati per creare una base di conoscenza per l'applicazione.
Include funzioni per estrarre testo dai file PDF, processare il testo,
creare embedding e memorizzare i dati in un vector store.
"""
import logging
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA

from rag_logic.ingestion.DocumentLoaderStrategy import WebLoaderStrategy, PDFLoaderStrategy, WordLoaderStrategy, \
    TextLoaderStrategy


class IngestionLayer(object):

    def __init__(self):
        persist_dir = "chroma_db"

        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.vectorstore = Chroma(
                    collection_name="chat_doc",
                    embedding_function=self.embeddings,
                    persist_directory=persist_dir)
        self.retriever_vs = self.vectorstore.as_retriever(search_type="similarity", k=3)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=200)
        self.llm = ChatOllama(model="llama3:latest", temperature=0.1, top_p=0.95, top_k=40)
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=self.retriever_vs, return_source_documents=True) #Todo: da aggiornare con la nuova api

        self.strategies = {
            ".pdf": PDFLoaderStrategy(),
            ".docx": WordLoaderStrategy(),
            ".txt": TextLoaderStrategy(),
            ".html": WebLoaderStrategy(),
            ".url": WebLoaderStrategy(),
        }

    def recreate(self):
        return  #Todo: ??

    def add_document_to_vectorstore(self, file_path: str):
        """
        Aggiunge un nuovo documento al vectorstore
        """
        ext = os.path.splitext(file_path)[1].lower()
        strategy = self.strategies.get(ext)

        if not strategy:
            raise ValueError(f"Nessuna strategia definita per il formato '{ext}'")

        print(f"[DEBUG] Loading document: {file_path}")
        documents = strategy.load(file_path)

        chunks = self.splitter.split_documents(documents)
        self.vectorstore.add_documents(chunks)
        print(f"[DEBUG] Added to vector store {len(chunks)} chunks")

    def delete_document_from_vectorstore(self, file_name):
        """
        Elimina i chunk associati a un file specifico dal vectorstore Chroma.

        Args:
            file_name (str): Il nome del file PDF da eliminare.
            persist_dir (str): La directory dove si trova il vectorstore.
        """

        file_name = os.path.splitext(file_name)[0]

        # Prima verifica quanti documenti ci sono con questo source
        results = self.vectorstore.get(where={"source": file_name})

        try:

            if not results['ids']:
                raise ValueError(f"Any chunk founded for file: '{file_name}'")

            ids_to_delete = []
            docs_in_store = self.vectorstore.get()

            target = os.path.splitext(file_name.lower())[0]
            for doc_id, doc_meta in zip(docs_in_store['ids'], docs_in_store['metadatas']):
                source = os.path.splitext(doc_meta.get("source", "").lower())[0]
                if source == target:
                    ids_to_delete.append(doc_id)

            print(f"[DEBUG] Trovati {len(ids_to_delete)} chunk da eliminare per il file '{file_name}'")
            self.vectorstore.delete(ids=ids_to_delete)
            print(f"[DEBUG] Eliminati {len(ids_to_delete)} chunk relativi a '{file_name}' dal vectorstore.")

        except ValueError as ve:
            logging.exception(ve, ve.with_traceback())
        except Exception as e:
            logging.exception(e, e.with_traceback())
