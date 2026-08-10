import unittest

from reqinsight.parsers.document_parser import DocumentParser


class TestRealDocument(unittest.TestCase):

    def test_real_srs_pdf(self):
        file_path = r"C:\Users\hp\Desktop\GM IU Work\Computer Science Project II\ReqInsight Project\ReqInsight\data\SELP_SRS.pdf"

        parser = DocumentParser()
        document = parser.parse(file_path)

        print("\n========================================")
        print("REAL PDF SRS PARSER TEST")
        print("========================================")
        print(f"File: {document.file_name}")
        print(f"Type: {document.file_type}")
        print(f"Characters extracted: {len(document.text)}")
        print("\nFirst 1000 characters:")
        print("----------------------------------------")
        print(document.text[:1000])
        print("----------------------------------------")

        self.assertEqual(document.file_type, "pdf")
        self.assertGreater(len(document.text), 0)

    def test_real_srs_docx(self):
        file_path = r"C:\Users\hp\Desktop\GM IU Work\Computer Science Project II\ReqInsight Project\ReqInsight\data\SELP_SRS.docx"

        parser = DocumentParser()
        document = parser.parse(file_path)

        print("\n========================================")
        print("REAL DOCX SRS PARSER TEST")
        print("========================================")
        print(f"File: {document.file_name}")
        print(f"Type: {document.file_type}")
        print(f"Characters extracted: {len(document.text)}")
        print("\nFirst 1000 characters:")
        print("----------------------------------------")
        print(document.text[:1000])
        print("----------------------------------------")

        self.assertEqual(document.file_type, "docx")
        self.assertGreater(len(document.text), 0)


if __name__ == "__main__":
    unittest.main()