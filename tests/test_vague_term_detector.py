import unittest

from reqinsight.nlp.vague_term_detector import VagueTermDetector


class TestVagueTermDetector(unittest.TestCase):

    def setUp(self):
        self.detector = VagueTermDetector()

    def test_detect_vague_term(self):

        text = "The system should provide a user-friendly interface."

        result = self.detector.detect(text)

        self.assertIn(
            "user-friendly",
            result
        )

    def test_detect_multiple_vague_terms(self):

        text = (
            "The system must respond quickly and provide "
            "appropriate recommendations."
        )

        result = self.detector.detect(text)

        self.assertIn("quickly", result)
        self.assertIn("appropriate", result)

    def test_no_vague_terms(self):

        text = (
            "The system must respond within 2 seconds "
            "and support 1,000 concurrent users."
        )

        result = self.detector.detect(text)

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()