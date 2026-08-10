from pathlib import Path

from reqinsight.models.document import Document
from reqinsight.parsers.base_parser import BaseDocumentParser
from reqinsight.parsers.docx_parser import DOCXParser
from reqinsight.parsers.pdf_parser import PDFParser
from reqinsight.parsers.txt_parser import TXTParser


class DocumentParser:
    """Facade that selects the appropriate parser for a document."""

    _PARSERS = {
        ".pdf": PDFParser,
        ".docx": DOCXParser,
        ".txt": TXTParser,
    }

    def parse(self, file_path: str) -> Document:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        extension = path.suffix.lower()

        parser_class = self._PARSERS.get(extension)

        if parser_class is None:
            supported = ", ".join(self._PARSERS.keys())

            raise ValueError(
                f"Unsupported file type '{extension}'. "
                f"Supported formats: {supported}"
            )

        parser: BaseDocumentParser = parser_class()

        return parser.parse(file_path)