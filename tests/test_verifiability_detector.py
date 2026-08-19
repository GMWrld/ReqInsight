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

    def test_detect_localization_requirement(self):

        text = (
            "The system must be localized for English "
            "and Spanish languages."
        )

        result = self.detector.detect(text)

        self.assertIn("must be localized", result["verification_terms"])
        self.assertTrue(result["verifiable"])

    def test_detect_non_verifiable_requirement(self):
        text = "The system should work properly under normal operating conditions."

        result = self.detector.detect(text)

        self.assertFalse(result["verifiable"])


    def test_detect_undefined_appropriate_response(self):
        text = (
            "The application must provide an appropriate response "
            "when a patient encounters an error."
        )

        result = self.detector.detect(text)

        self.assertFalse(result["verifiable"])


    def test_detect_subjective_usability_requirement(self):
        text = "The interface should be easy for doctors and nurses to use."

        result = self.detector.detect(text)

        self.assertFalse(result["verifiable"])


    def test_detect_suitable_performance_requirement(self):
        text = "The system must maintain suitable performance during peak usage."

        result = self.detector.detect(text)

        self.assertFalse(result["verifiable"])


    def test_detect_efficiency_requirement(self):
        text = "The system should handle patient records efficiently."

        result = self.detector.detect(text)

        self.assertFalse(result["verifiable"])


    def test_detect_verifiable_display_requirement(self):
        text = "The system must display the patient's current heart rate on the dashboard."

        result = self.detector.detect(text)

        self.assertTrue(result["verifiable"])


    def test_detect_verifiable_standard_requirement(self):
        text = "The system must support HL7 FHIR for exchanging patient clinical data."

        result = self.detector.detect(text)

        self.assertTrue(result["verifiable"])


    def test_detect_verifiable_password_reset(self):
        text = "The system must allow doctors to reset their passwords using an OTP."

        result = self.detector.detect(text)

        self.assertTrue(result["verifiable"])


    def test_detect_verifiable_localization(self):
        text = (
            "The system must support English, Spanish, and Mandarin "
            "user interfaces."
        )

        result = self.detector.detect(text)

        self.assertTrue(result["verifiable"])


if __name__ == "__main__":
    unittest.main()