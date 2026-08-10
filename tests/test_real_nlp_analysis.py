import unittest

from reqinsight.parsers.document_parser import DocumentParser
from reqinsight.analysis.requirement_extractor import RequirementExtractor
from reqinsight.nlp.requirement_analyzer import RequirementAnalyzer


class TestRealNLPAnalysis(unittest.TestCase):

    def test_analyze_real_srs(self):

        file_path = r"C:\Users\hp\Desktop\GM IU Work\Computer Science Project II\ReqInsight Project\ReqInsight\data\SELP_SRS.pdf"

        parser = DocumentParser()
        document = parser.parse(file_path)

        extractor = RequirementExtractor()
        requirements = extractor.extract(document)

        analyzer = RequirementAnalyzer()

        print("\n========================================")
        print("REAL SRS NLP ANALYSIS TEST")
        print("========================================")

        print(f"Document: {document.file_name}")
        print(f"Requirements: {len(requirements)}")

        print("\n----------------------------------------")
        print("NLP FEATURES")
        print("----------------------------------------")

        for requirement in requirements:

            result = analyzer.analyze(requirement)

            print(
                f"{result['requirement_id']} | "
                f"Words: {result['word_count']} | "
                f"Characters: {result['character_count']} | "
                f"Modal: {result['modal_words']} | "
                f"Vague: {result['vague_terms']}",
                f"Quantifiable: {result['quantifiable_constraints']}"
            )

        self.assertEqual(len(requirements), 39)

        for requirement in requirements:

            result = analyzer.analyze(requirement)

            self.assertGreater(
                result["word_count"],
                0
            )


if __name__ == "__main__":
    unittest.main()