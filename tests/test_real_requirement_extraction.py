import unittest

from reqinsight.parsers.document_parser import DocumentParser
from reqinsight.analysis.requirement_extractor import RequirementExtractor


class TestRealRequirementExtraction(unittest.TestCase):

    def test_extract_from_real_srs(self):

        file_path = r"C:\Users\hp\Desktop\GM IU Work\Computer Science Project II\ReqInsight Project\ReqInsight\data\SELP_SRS.pdf"

        parser = DocumentParser()
        document = parser.parse(file_path)

        extractor = RequirementExtractor()
        requirements = extractor.extract(document)

        print("\n========================================")
        print("REAL SRS REQUIREMENT EXTRACTION TEST")
        print("========================================")

        print(f"Document: {document.file_name}")
        print(f"Characters: {len(document.text)}")
        print(f"Requirements detected: {len(requirements)}")

        print("\n----------------------------------------")
        print("EXTRACTED REQUIREMENTS")
        print("----------------------------------------")

        for number, requirement in enumerate(requirements, start=1):

            identifier = requirement.requirement_id or "NO-ID"

            print(
                f"{number:02d}. "
                f"[{identifier}] "
                f"{requirement.text}"
            )

        print("----------------------------------------")

        self.assertGreater(len(requirements), 0)


if __name__ == "__main__":
    unittest.main()