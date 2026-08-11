import unittest
from pathlib import Path

from reqinsight.application.analysis_service import (
    RequirementAnalysisService
)


class TestRequirementAnalysisService(unittest.TestCase):

    def setUp(self):
        self.service = RequirementAnalysisService()

        self.file_path = (
            Path("data") / "SELP_SRS.pdf"
        )

    def test_analyze_real_srs(self):

        result = self.service.analyze(
            self.file_path
        )

        # Document information
        self.assertEqual(
            result["document"]["file_name"],
            "SELP_SRS.pdf"
        )

        self.assertEqual(
            result["document"]["requirement_count"],
            39
        )

        # Requirement results
        self.assertEqual(
            len(result["requirements"]),
            39
        )

        # Document score
        self.assertEqual(
            result["summary"]["score"],
            99.23
        )

        self.assertEqual(
            result["summary"]["classification"],
            "EXCELLENT"
        )

    def test_requirement_results_contain_expected_fields(self):

        result = self.service.analyze(
            self.file_path
        )

        first_requirement = result["requirements"][0]

        self.assertIn(
            "requirement_id",
            first_requirement
        )

        self.assertIn(
            "text",
            first_requirement
        )

        self.assertIn(
            "analysis",
            first_requirement
        )

        self.assertIn(
            "findings",
            first_requirement
        )

        self.assertIn(
            "score",
            first_requirement
        )

        self.assertIn(
            "classification",
            first_requirement
        )

    def test_real_srs_quality_distribution(self):

        result = self.service.analyze(
            self.file_path
        )

        summary = result["summary"]

        self.assertEqual(
            summary["total_requirements"],
            39
        )

        self.assertEqual(
            summary["excellent"],
            37
        )

        self.assertEqual(
            summary["good"],
            2
        )

        self.assertEqual(
            summary["needs_review"],
            0
        )

        self.assertEqual(
            summary["poor"],
            0
        )


if __name__ == "__main__":
    unittest.main()