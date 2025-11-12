from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

from rag_logic.ingestion.IDocumentLoader import DocumentLoaderStrategy


class PDFLoaderStrategy(DocumentLoaderStrategy):
    def load(self, file_path):
        loader = PyPDFLoader(file_path)
        return loader.load()

class WordLoaderStrategy(DocumentLoaderStrategy):
    def load(self, file_path):
        loader = UnstructuredWordDocumentLoader(file_path)
        return loader.load()

class TextLoaderStrategy(DocumentLoaderStrategy):
    def load(self, file_path):
        loader = TextLoader(file_path)
        return loader.load()

class WebLoaderStrategy(DocumentLoaderStrategy):
    def load(self, url):
        loader = WebBaseLoader(url)
        return loader.load()

class CSVLoaderStrategy(DocumentLoaderStrategy):
    def load(self, file_path: str):
        loader = CSVLoader(
            file_path,
            csv_args={
                "delimiter": ",",
                "quotechar": '"'
            }
        )
        return loader.load()
