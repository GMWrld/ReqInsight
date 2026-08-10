from pathlib import Path

from pypdf import PdfReader

from reqinsight.models.document import Document
from reqinsight.parsers.base_parser import BaseDocumentParser


class PDFParser(BaseDocumentParser):
    """Parser for text-based PDF files."""

    def parse(self, file_path: str) -> Document:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text.strip())

        text = "\n".join(pages)

        document = Document(file_path)
        document.text = text

        return document