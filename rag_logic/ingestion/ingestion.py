import logging
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_classic.chains import RetrievalQA
#from langchain.chains.retrieval import create_retrieval_chain

from rag_logic.ingestion.DocumentLoaderStrategy import *
from rag_logic.llm.Ollama import Ollama

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

class IngestionFlow(object):
    """
    The IngestionFlow class manages the full ingestion process of external documents
    into a vector-based knowledge store. It performs the following tasks:
     - Load text from various file formats via loader strategies
     - Split documents into manageable chunks
     - Generate embeddings for semantic search
     - Store and persist chunks in a Chroma vector database
     - Provide a retrieval-enabled QA chain integrated with an LLM
    """

    def __init__(self, notebook_id: str):
        """
        Initializes the ingestion flow with embedding, vector store, retriever,
        and large language model (LLM) configurations.
        """

        self.persist_dir = f"chroma_db/{notebook_id}"

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

        self.vectorstore = Chroma(
                    collection_name="chat_docs",
                    embedding_function=self.embeddings,
                    persist_directory=self.persist_dir)

        self.retriever_vs = self.vectorstore.as_retriever(search_type="similarity", k=3)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=200)
        self.llm = Ollama() #ChatOllama(model="llama3:latest", temperature=0.1, top_p=0.95, top_k=40)
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=self.retriever_vs, return_source_documents=True)
        #self.qa_chain = create_retrieval_chain(self.retriever_vs, self.llm)

        self.strategies = {
            ".pdf": PDFLoaderStrategy(),
            ".docx": WordLoaderStrategy(),
            ".txt": TextLoaderStrategy(),
            ".html": WebLoaderStrategy(),
            ".url": WebLoaderStrategy(),
            ".csv": CSVLoaderStrategy(),
        }

        logger.info(f"IngestionFlow initialized for notebook '{notebook_id}'.")

    def reload_vectorstore(self):
        """

        """
        if not os.path.exists(self.persist_dir):
            raise FileNotFoundError(f"Nessun database Chroma trovato in '{self.persist_dir}'.")

        logger.info(f"Riapertura vectorstore da '{self.persist_dir}'...")

        self.vectorstore = Chroma(
            collection_name="chat_docs",
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir
        )

        self.retriever_vs = self.vectorstore.as_retriever(search_type="similarity", k=3)
        self.qa_chain.retriever = self.retriever_vs

        logger.info("Vectorstore ricaricato con successo.")

    def add_document_to_vectorstore(self, file_path: str):
        """
        Adds a new document to the vector store by:
          1. Loading it using the appropriate strategy.
          2. Splitting into smaller text chunks.
          3. Embedding and storing them in Chroma.

        Args:
            file_path (str): Path to the input file.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        ext = os.path.splitext(file_path)[1].lower()
        strategy = self.strategies.get(ext)

        if not strategy:
            raise ValueError(f"No strategy defined for file format '{ext}'")

        logger.info(f"Loading document: {file_path}")

        documents = strategy.load(file_path)

        for doc in documents:
            if "source" not in doc.metadata:
                doc.metadata["source"] = file_path

        chunks = self.splitter.split_documents(documents)

        if not chunks:
            logger.warning(f"No chunks generated from document '{file_path}'.")
            return

        self.vectorstore.add_documents(chunks)

        logger.info(f"Added {len(chunks)} chunks from '{file_path}' to vectorstore.")

    def delete_document_from_vectorstore(self, file_name: str):
        """
        Deletes all chunks associated with a specific file from the Chroma vector store.

        Args:
            file_name (str): The name of the source file to remove.
        """

        file_name = os.path.splitext(file_name)[0]

        try:
            docs_in_store = self.vectorstore.get()
            ids_to_delete = []

            for doc_id, doc_meta in zip(docs_in_store.get("ids", []), docs_in_store.get("metadatas", [])):
                source = os.path.splitext(doc_meta.get("source", "").lower())[0]
                if source == file_name:
                    ids_to_delete.append(doc_id)

            if not ids_to_delete:
                logger.info(f"No chunks found for '{file_name}'. Nothing to delete.")
                return

            self.vectorstore.delete(ids=ids_to_delete)
            logger.info(f"Deleted {len(ids_to_delete)} chunks for file '{file_name}' from vectorstore.")

        except ValueError as ve:
            logger.exception(ve)
        except Exception as e:
            logger.exception(e)
