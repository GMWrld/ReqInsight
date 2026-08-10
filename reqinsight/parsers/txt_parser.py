from pathlib import Path

from reqinsight.models.document import Document
from reqinsight.parsers.base_parser import BaseDocumentParser


class TXTParser(BaseDocumentParser):
    """Parser for plain-text files."""

    def parse(self, file_path: str) -> Document:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        text = path.read_text(encoding="utf-8")

        document = Document(file_path)
        document.text = text

        return document