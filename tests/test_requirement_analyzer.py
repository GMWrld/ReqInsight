import unittest

from reqinsight.models.requirement import Requirement
from reqinsight.nlp.requirement_analyzer import RequirementAnalyzer


class TestRequirementAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = RequirementAnalyzer()

    def test_requirement_analysis(self):

        requirement = Requirement(
            requirement_id="FR-01",
            text="The system must allow users to register using an email address."
        )

        result = self.analyzer.analyze(requirement)

        self.assertEqual(
            result["requirement_id"],
            "FR-01"
        )

        self.assertGreater(
            result["word_count"],
            0
        )

        self.assertGreater(
            result["character_count"],
            0
        )

        self.assertEqual(
            result["modal_words"],
            ["must"]
        )

        self.assertTrue(
            result["has_modal"]
        )

    def test_requirement_without_modal(self):

        requirement = Requirement(
            requirement_id="TEST-01",
            text="The platform provides online learning services."
        )

        result = self.analyzer.analyze(requirement)

        self.assertEqual(
            result["modal_words"],
            []
        )

        self.assertFalse(
            result["has_modal"]
        )

    def test_detect_vague_terms(self):

        requirement = Requirement(
            requirement_id="TEST-02",
            text="The system must provide a user-friendly interface."
        )

        result = self.analyzer.analyze(requirement)

        self.assertEqual(
            result["vague_terms"],
            ["user-friendly"]
        )

        self.assertTrue(
            result["has_vague_terms"]
        )


if __name__ == "__main__":
    unittest.main()