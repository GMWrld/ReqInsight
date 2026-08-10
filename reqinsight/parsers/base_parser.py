from abc import ABC, abstractmethod

from reqinsight.models.document import Document


class BaseDocumentParser(ABC):
    """Abstract base class for all document parsers."""

    @abstractmethod
    def parse(self, file_path: str) -> Document:
        """
        Parse a document and return a Document object.

        Args:
            file_path: Path to the document.

        Returns:
            Parsed Document object.
        """
        pass