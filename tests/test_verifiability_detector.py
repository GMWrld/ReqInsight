import unittest

from reqinsight.analysis.verifiability_detector import VerifiabilityDetector


class TestVerifiabilityDetector(unittest.TestCase):

    def setUp(self):
        self.detector = VerifiabilityDetector()

    def test_detect_technical_criterion(self):

        text = (
            "All data transmitted between the client and server "
            "must be encrypted using TLS 1.3."
        )

        result = self.detector.detect(text)

        self.assertIn("tls", result["technical_criteria"])
        self.assertTrue(result["verifiable"])

    def test_detect_bcrypt(self):

        text = "User passwords must be hashed using BCrypt."

        result = self.detector.detect(text)

        self.assertIn("bcrypt", result["technical_criteria"])
        self.assertTrue(result["verifiable"])

    def test_detect_gdpr(self):

        text = (
            "User data privacy must comply with GDPR "
            "regulations."
        )

        result = self.detector.detect(text)

        self.assertIn("gdpr", result["technical_criteria"])
        self.assertTrue(result["verifiable"])

    def test_detect_verification_term(self):

        text = (
            "The system must display a clear error message "
            "when an upload fails."
        )

        result = self.detector.detect(text)

        self.assertIn(
            "must display",
            result["verification_terms"]
        )

        self.assertTrue(result["verifiable"])

    def test_no_verifiability_indicator(self):

        text = (
            "The system should be easy and user friendly."
        )

        result = self.detector.detect(text)

        self.assertEqual(result["technical_criteria"], [])
        self.assertEqual(result["verification_terms"], [])
        self.assertFalse(result["verifiable"])


if __name__ == "__main__":
    unittest.main()