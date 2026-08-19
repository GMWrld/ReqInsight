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

    # ---------------------------------------------------------
    # Additional vague terminology discovered during evaluation
    # ---------------------------------------------------------

    def test_detect_secure_terms(self):

        text = (
            "The system must store patient information securely "
            "and provide secure access to clinical records."
        )

        result = self.detector.detect(text)

        self.assertIn("securely", result)
        self.assertIn("secure", result)

    def test_detect_detailed_term(self):

        text = "The system must maintain detailed patient-record access logs."

        result = self.detector.detect(text)

        self.assertIn("detailed", result)

    def test_detect_prominent_term(self):

        text = (
            "The system must display critical allergies prominently "
            "across all screens."
        )

        result = self.detector.detect(text)

        self.assertIn("prominently", result)

    def test_detect_clear_term(self):

        text = (
            "The system must display a clear error message "
            "when an upload fails."
        )

        result = self.detector.detect(text)

        self.assertIn("clear", result)

    def test_detect_consistent_term(self):

        text = (
            "The interface must provide a consistent look and feel "
            "across all screens."
        )

        result = self.detector.detect(text)

        self.assertIn("consistent", result)

    def test_detect_low_technical_proficiency(self):

        text = (
            "The system must be designed for low technical proficiency "
            "users with appropriate accessibility support."
        )

        result = self.detector.detect(text)

        self.assertIn("low technical proficiency", result)

    def test_do_not_flag_fhir_name(self):

        text = (
            "The system must support HL7 FHIR "
            "(Fast Healthcare Interoperability Resources) "
            "for exchanging clinical data."
        )

        result = self.detector.detect(text)

        self.assertNotIn("fast", result)


if __name__ == "__main__":
    unittest.main()