import unittest

from reqinsight.quality.quality_scorer import QualityScorer


class TestQualityScorer(unittest.TestCase):

    def setUp(self):
        self.scorer = QualityScorer()

    def test_perfect_requirement(self):

        result = self.scorer.score([])

        self.assertEqual(result["score"], 100)
        self.assertEqual(
            result["classification"],
            "EXCELLENT"
        )

    def test_single_warning(self):

        findings = [
            {
                "rule": "MODAL-CONSISTENCY"
            }
        ]

        result = self.scorer.score(findings)

        self.assertEqual(result["score"], 85)
        self.assertEqual(
            result["classification"],
            "GOOD"
        )

    def test_multiple_findings(self):

        findings = [
            {
                "rule": "MODAL-CONSISTENCY"
            },
            {
                "rule": "VAGUENESS"
            },
        ]

        result = self.scorer.score(findings)

        self.assertEqual(result["score"], 70)
        self.assertEqual(
            result["classification"],
            "NEEDS REVIEW"
        )

    def test_unknown_rule_does_not_reduce_score(self):

        findings = [
            {
                "rule": "UNKNOWN-RULE"
            }
        ]

        result = self.scorer.score(findings)

        self.assertEqual(result["score"], 100)

    def test_score_cannot_be_negative(self):

        findings = [
            {"rule": "MODAL-CONSISTENCY"},
            {"rule": "MODAL-CONSISTENCY"},
            {"rule": "VAGUENESS"},
            {"rule": "VAGUENESS"},
            {"rule": "MEASURABILITY"},
            {"rule": "MEASURABILITY"},
            {"rule": "VERIFIABILITY"},
            {"rule": "VERIFIABILITY"},
        ]

        result = self.scorer.score(findings)

        self.assertEqual(result["score"], 0)
        self.assertEqual(
            result["classification"],
            "POOR"
        )

    def test_classification_boundaries(self):

        self.assertEqual(
            self.scorer.classify(100),
            "EXCELLENT"
        )

        self.assertEqual(
            self.scorer.classify(90),
            "EXCELLENT"
        )

        self.assertEqual(
            self.scorer.classify(89),
            "GOOD"
        )

        self.assertEqual(
            self.scorer.classify(80),
            "GOOD"
        )

        self.assertEqual(
            self.scorer.classify(79),
            "NEEDS REVIEW"
        )

        self.assertEqual(
            self.scorer.classify(70),
            "NEEDS REVIEW"
        )

        self.assertEqual(
            self.scorer.classify(69),
            "POOR"
        )


if __name__ == "__main__":
    unittest.main()