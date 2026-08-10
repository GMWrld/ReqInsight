import unittest

from reqinsight.analysis.requirement_extractor import RequirementExtractor
from reqinsight.models.document import Document


class TestRequirementExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = RequirementExtractor()

    def test_extract_requirement_with_identifier(self):
        document = Document("test.txt")
        document.text = """
        FR-01: The system must authenticate users.
        FR-02: The system must lock accounts after five failed attempts.
        """

        requirements = self.extractor.extract(document)

        self.assertEqual(len(requirements), 2)

        self.assertEqual(
            requirements[0].requirement_id,
            "FR-01"
        )

        self.assertEqual(
            requirements[0].text,
            "The system must authenticate users."
        )

    def test_extract_requirement_without_identifier(self):
        document = Document("test.txt")
        document.text = """
        The system shall authenticate users.
        The application must encrypt customer data.
        """

        requirements = self.extractor.extract(document)

        self.assertEqual(len(requirements), 2)

        self.assertIsNone(
            requirements[0].requirement_id
        )

    def test_ignore_non_requirement_text(self):
        document = Document("test.txt")
        document.text = """
        The purpose of this document is to describe the system.
        The development team will use this document.
        The system shall authenticate users.
        """

        requirements = self.extractor.extract(document)

        self.assertEqual(len(requirements), 1)
        self.assertEqual(
            requirements[0].text,
            "The system shall authenticate users."
        )

    def test_reconstruct_multiline_requirement(self):
        document = Document("test.txt")

        document.text = """
        FR-17: The system must analyze a student's quiz results and viewing speed to recommend
        supplementary content.

        FR-18: If a student scores below 60% on a quiz, the system must recommend a
        Remedial Video on the failed topic.
        """

        requirements = self.extractor.extract(document)

        self.assertEqual(len(requirements), 2)

        self.assertEqual(
            requirements[0].requirement_id,
            "FR-17"
        )

        self.assertEqual(
            requirements[0].text,
            "The system must analyze a student's quiz results and viewing speed to recommend supplementary content."
        )

        self.assertEqual(
            requirements[1].requirement_id,
            "FR-18"
        )

        self.assertEqual(
            requirements[1].text,
            "If a student scores below 60% on a quiz, the system must recommend a Remedial Video on the failed topic."
        )

    def test_stop_at_structural_heading(self):
        document = Document("test.txt")

        document.text = """
        FR-04: The system must lock user accounts after 5 unsuccessful login attempts.

        3.1.2 Course Management (Educator)

        FR-05: Educators must be able to create a new course.
        """

        requirements = self.extractor.extract(document)

        self.assertEqual(len(requirements), 2)

        self.assertEqual(
            requirements[0].text,
            "The system must lock user accounts after 5 unsuccessful login attempts."
        )

        self.assertEqual(
            requirements[1].text,
            "Educators must be able to create a new course."
        )

    def test_remove_embedded_structural_heading(self):
        document = Document("test.txt")

        document.text = """
        FR-04: The system must lock user accounts after 5 unsuccessful login attempts. 3.1.2 Course Management (Educator)
        FR-05: Educators must be able to create a new course.
        """

        requirements = self.extractor.extract(document)

        self.assertEqual(len(requirements), 2)

        self.assertEqual(
            requirements[0].text,
            "The system must lock user accounts after 5 unsuccessful login attempts."
        )

        self.assertEqual(
            requirements[1].text,
            "Educators must be able to create a new course."
        )

    def test_remove_embedded_appendix(self):
        document = Document("test.txt")

        document.text = """
        NFR-11: The system must display a clear error message and allow the user to retry without losing the course setup. Appendices Appendix A: Database Schema Diagram (To be drafted).
        """

        requirements = self.extractor.extract(document)

        self.assertEqual(len(requirements), 1)

        self.assertEqual(
            requirements[0].text,
            "The system must display a clear error message and allow the user to retry without losing the course setup."
        )

if __name__ == "__main__":
    unittest.main()