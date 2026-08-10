import unittest

from reqinsight.nlp.quantifiable_constraint_detector import (
    QuantifiableConstraintDetector
)


class TestQuantifiableConstraintDetector(unittest.TestCase):

    def setUp(self):
        self.detector = QuantifiableConstraintDetector()

    def test_detect_percentage(self):

        text = "The system must maintain 99.9% uptime."

        result = self.detector.detect(text)

        self.assertIn("99.9%", result)

    def test_detect_time_constraint(self):

        text = "The system must respond within 2 seconds."

        result = self.detector.detect(text)

        self.assertIn("2 seconds", result)

    def test_detect_multiple_constraints(self):

        text = (
            "The platform must support up to 1,000 users "
            "with a response time under 500ms."
        )

        result = self.detector.detect(text)

        self.assertIn("1,000 users", result)
        self.assertIn("500ms", result)

    def test_no_quantifiable_constraint(self):

        text = "The system must allow users to register."

        result = self.detector.detect(text)

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()