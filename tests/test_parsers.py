import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from reqinsight.parsers.document_parser import DocumentParser


class TestDocumentParser(unittest.TestCase):

    def test_txt_parser(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_srs.txt"

            file_path.write_text(
                "The system shall authenticate users.",
                encoding="utf-8"
            )

            parser = DocumentParser()
            document = parser.parse(str(file_path))

            self.assertEqual(document.file_type, "txt")
            self.assertIn(
                "The system shall authenticate users.",
                document.text
            )

    def test_unsupported_file_type(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_srs.xlsx"
            file_path.write_text("test", encoding="utf-8")

            parser = DocumentParser()

            with self.assertRaises(ValueError):
                parser.parse(str(file_path))


if __name__ == "__main__":
    unittest.main()