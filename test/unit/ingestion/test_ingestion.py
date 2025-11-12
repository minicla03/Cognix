import unittest
from unittest.mock import MagicMock, patch
from rag_logic.ingestion.ingestion import IngestionFlow


class TestIngestionFlow(unittest.TestCase):
    """
    Unit test suite for the IngestionFlow class.
    Uses mock objects to isolate external dependencies such as
    vector stores, embedding models, and LLMs.
    """

    def setUp(self):
        """Initialize an IngestionFlow instance with mocks for vectorstore and strategies."""
        self.flow = IngestionFlow()

        # Mock the vectorstore to avoid real persistence
        self.flow.vectorstore = MagicMock()
        self.flow.vectorstore.get.return_value = {
            "ids": ["1", "2"],
            "metadatas": [{"source": "doc1.pdf"}, {"source": "doc2.pdf"}]
        }

        # Mock embedding and QA chain
        self.flow.embeddings = MagicMock()
        self.flow.qa_chain = MagicMock()

        # Mock file strategies
        mock_strategy = MagicMock()
        mock_strategy.load.return_value = [{"page_content": "mock text"}]
        self.flow.strategies = {
            ".pdf": mock_strategy,
            ".txt": mock_strategy
        }

        # Mock text splitter
        self.flow.splitter = MagicMock()
        self.flow.splitter.split_documents.return_value = [
            {"page_content": "chunk1"},
            {"page_content": "chunk2"},
        ]

    def test_add_document_to_vectorstore_success(self):
        """Ensure add_document_to_vectorstore adds chunks correctly."""
        with patch("os.path.exists", return_value=True):
            self.flow.add_document_to_vectorstore("sample.pdf")

        self.flow.vectorstore.add_documents.assert_called_once()

    def test_add_document_with_invalid_extension(self):
        """Ensure unsupported file extensions raise a ValueError."""
        with self.assertRaises(ValueError):
            with patch("os.path.exists", return_value=True):
                self.flow.add_document_to_vectorstore("sample.xyz")

    def test_add_document_not_found(self):
        """Ensure missing files raise a FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            self.flow.add_document_to_vectorstore("missing.pdf")

    def test_delete_document_found(self):
        """Ensure delete_document_from_vectorstore removes correct chunks."""
        self.flow.vectorstore.get.return_value = {
            "ids": ["1", "2", "3"],
            "metadatas": [
                {"source": "doc1"},
                {"source": "doc1"},
                {"source": "otherdoc"},
            ]
        }

        self.flow.delete_document_from_vectorstore("doc1.pdf")
        self.flow.vectorstore.delete.assert_called_once()

    def test_delete_document_not_found(self):
        """Ensure no error if document not found in vectorstore."""
        self.flow.vectorstore.get.return_value = {"ids": [], "metadatas": []}

        # Should log but not raise
        self.flow.delete_document_from_vectorstore("nonexistent.pdf")
        self.flow.vectorstore.delete.assert_not_called()

    def test_logger_output(self):
        """Ensure logging occurs during initialization."""
        with self.assertLogs(level="INFO") as log:
            IngestionFlow()
        self.assertTrue(any("initialized successfully" in msg for msg in log.output))

if __name__ == "__main__":
    unittest.main()
