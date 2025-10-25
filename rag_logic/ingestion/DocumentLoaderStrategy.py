from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, WebBaseLoader

from rag_logic.ingestion.IDocumentLoader import DocumentLoaderStrategy


class PDFLoaderStrategy(DocumentLoaderStrategy):
    def load(self, file_path):
        loader = PyPDFLoader(file_path)
        return loader.load()

class WordLoaderStrategy(DocumentLoaderStrategy):
    def load(self, file_path):
        loader = Docx2txtLoader(file_path)
        return loader.load()

class TextLoaderStrategy(DocumentLoaderStrategy):
    def load(self, file_path):
        loader = TextLoader(file_path)
        return loader.load()

class WebLoaderStrategy(DocumentLoaderStrategy):
    def load(self, url):
        loader = WebBaseLoader(url)
        return loader.load()
