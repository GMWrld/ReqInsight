import unittest

from reqinsight.models.document import Document
from reqinsight.models.requirement import Requirement


class TestModels(unittest.TestCase):

    def test_document_initialization(self):
        document = Document("sample_srs.pdf")

        self.assertEqual(document.file_name, "sample_srs.pdf")
        self.assertEqual(document.file_type, "pdf")
        self.assertEqual(document.requirement_count, 0)

    def test_add_requirement(self):
        document = Document("sample_srs.pdf")
        requirement = Requirement(
            requirement_id="FR-01",
            text="The system shall authenticate users."
        )

        document.add_requirement(requirement)

        self.assertEqual(document.requirement_count, 1)
        self.assertEqual(document.requirements[0].requirement_id, "FR-01")


if __name__ == "__main__":
    unittest.main()
