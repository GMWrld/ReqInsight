import unittest

from reqinsight.quality.document_quality_scorer import (
    DocumentQualityScorer
)


class TestDocumentQualityScorer(unittest.TestCase):

    def setUp(self):
        self.scorer = DocumentQualityScorer()

    def test_single_requirement(self):

        results = [
            {
                "score": 100,
                "classification": "EXCELLENT"
            }
        ]

        summary = self.scorer.summarize(results)

        self.assertEqual(summary["score"], 100)
        self.assertEqual(
            summary["classification"],
            "EXCELLENT"
        )

    def test_average_score(self):

        results = [
            {
                "score": 100,
                "classification": "EXCELLENT"
            },
            {
                "score": 85,
                "classification": "GOOD"
            }
        ]

        summary = self.scorer.summarize(results)

        self.assertEqual(summary["score"], 92.5)
        self.assertEqual(
            summary["classification"],
            "EXCELLENT"
        )

    def test_empty_document(self):

        summary = self.scorer.summarize([])

        self.assertEqual(summary["score"], 0)
        self.assertEqual(
            summary["classification"],
            "POOR"
        )
        self.assertEqual(
            summary["total_requirements"],
            0
        )

    def test_classification_counts(self):

        results = [
            {
                "score": 100,
                "classification": "EXCELLENT"
            },
            {
                "score": 100,
                "classification": "EXCELLENT"
            },
            {
                "score": 85,
                "classification": "GOOD"
            },
            {
                "score": 70,
                "classification": "NEEDS REVIEW"
            },
            {
                "score": 50,
                "classification": "POOR"
            }
        ]

        summary = self.scorer.summarize(results)

        self.assertEqual(summary["total_requirements"], 5)
        self.assertEqual(summary["excellent"], 2)
        self.assertEqual(summary["good"], 1)
        self.assertEqual(summary["needs_review"], 1)
        self.assertEqual(summary["poor"], 1)

    def test_score_is_rounded(self):

        results = [
            {
                "score": 100,
                "classification": "EXCELLENT"
            },
            {
                "score": 85,
                "classification": "GOOD"
            },
            {
                "score": 100,
                "classification": "EXCELLENT"
            }
        ]

        summary = self.scorer.summarize(results)

        self.assertEqual(summary["score"], 95.0)


if __name__ == "__main__":
    unittest.main()