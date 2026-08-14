import unittest

from reqinsight.analysis.requirement_candidate_detector import (
    RequirementCandidateDetector,
)


class TestRequirementCandidateDetector(unittest.TestCase):

    def setUp(self):
        self.detector = RequirementCandidateDetector()

    def assert_candidate(self, text):
        result = self.detector.detect(text)

        self.assertTrue(
            result.is_candidate,
            msg=f"Expected candidate: {text!r}"
        )

        self.assertGreater(
            result.confidence,
            0
        )

    def assert_not_candidate(self, text):
        result = self.detector.detect(text)

        self.assertFalse(
            result.is_candidate,
            msg=f"Unexpected candidate: {text!r}"
        )

    def test_standard_requirement(self):
        self.assert_candidate(
            "FR-01: The system must allow users to register."
        )

    def test_modular_requirement(self):
        self.assert_candidate(
            "FR-A-01: The system must create patient records."
        )

    def test_arbitrary_requirement_id(self):
        self.assert_candidate(
            "REQ-AUTH-002: The system must support MFA."
        )

    def test_requirement_without_id(self):
        self.assert_candidate(
            "Customers should be able to add products to their cart."
        )

    def test_can_capability(self):
        self.assert_candidate(
            "Users can search for products by name."
        )

    def test_able_to_capability(self):
        self.assert_candidate(
            "Customers are able to download invoices."
        )

    def test_allows_capability(self):
        self.assert_candidate(
            "The application allows users to reset passwords."
        )

    def test_user_story(self):
        self.assert_candidate(
            "As a customer, I want to track my order."
        )

    def test_performance_requirement(self):
        self.assert_candidate(
            "Response time must remain below 2 seconds."
        )

    def test_security_requirement(self):
        self.assert_candidate(
            "All transmitted data shall use TLS 1.3."
        )

    def test_system_capability(self):
        self.assert_candidate(
            "The platform provides order tracking."
        )

    def test_document_description_is_not_requirement(self):
        self.assert_not_candidate(
            "This document describes the proposed e-commerce platform."
        )

    def test_project_statement_is_not_requirement(self):
        self.assert_not_candidate(
            "The project team will use Agile methodology."
        )

    def test_implementation_statement_is_not_requirement(self):
        self.assert_not_candidate(
            "The application was developed using Python."
        )

    def test_appendix_heading_is_not_requirement(self):
        self.assert_not_candidate(
            "Appendix A: Data Dictionary"
        )

    def test_document_purpose_is_not_requirement(self):
        self.assert_not_candidate(
            "The purpose of this Software Requirements Specification (SRS) "
            "document is to provide a detailed description."
        )

    def test_modal_definition_is_not_requirement(self):
        self.assert_not_candidate(
            "Must: Indicates a mandatory requirement."
        )

    def test_should_definition_is_not_requirement(self):
        self.assert_not_candidate(
            "Should: Indicates a recommended requirement."
        )

    def test_may_definition_is_not_requirement(self):
        self.assert_not_candidate(
            "May: Indicates an optional requirement."
        )

    def test_product_description_is_not_requirement(self):
        self.assert_not_candidate(
            "The SELP is a web-based application designed to facilitate "
            "virtual learning."
        )

    def test_product_description_continuation_is_not_requirement(self):
        self.assert_not_candidate(
            "video lectures, create quizzes, and track student progress."
        )

    def test_document_reference_title_is_not_requirement(self):
        self.assert_not_candidate(
            "SELP Business Requirements Document (BRD) v1.0."
        )

    def test_stakeholder_need_is_not_requirement(self):
        self.assert_not_candidate(
            "Students: Need an intuitive interface to access courses, "
            "complete assessments, and receive feedback."
        )

    def test_dependency_statement_is_not_requirement(self):
        self.assert_not_candidate(
            "The system relies on a third-party Cloud Storage Service "
            "(e.g., AWS S3) for hosting media files."
        )


if __name__ == "__main__":
    unittest.main()