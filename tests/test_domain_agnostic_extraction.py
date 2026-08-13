import unittest

from reqinsight.analysis.requirement_extractor import RequirementExtractor
from reqinsight.models.document import Document


class TestDomainAgnosticExtraction(unittest.TestCase):

    def setUp(self):
        self.extractor = RequirementExtractor()

    def extract(self, text):
        document = Document(
            file_path="test.txt",
            text=text
        )
        return self.extractor.extract(document)

    def ids(self, requirements):
        return [
            requirement.requirement_id
            for requirement in requirements
        ]

    def texts(self, requirements):
        return [
            requirement.text
            for requirement in requirements
        ]

    # ---------------------------------------------------------
    # 1. STANDARD NUMBERED REQUIREMENTS
    # ---------------------------------------------------------

    def test_standard_requirement_ids(self):

        requirements = self.extract(
            """
            FR-01: The system must allow users to register.
            FR-02: The system must allow users to log in.
            NFR-01: The system must respond within 2 seconds.
            """
        )

        self.assertEqual(
            len(requirements),
            3
        )

        self.assertEqual(
            self.ids(requirements),
            [
                "FR-01",
                "FR-02",
                "NFR-01",
            ]
        )

    # ---------------------------------------------------------
    # 2. MODULAR REQUIREMENT IDs
    # ---------------------------------------------------------

    def test_modular_requirement_ids(self):

        requirements = self.extract(
            """
            FR-A-01: The system must create patient records.
            FR-A-02: The system must update patient records.
            FR-B-01: The system must process payments.
            FR-C-04: The system must generate reports.
            """
        )

        self.assertEqual(
            len(requirements),
            4
        )

        self.assertEqual(
            self.ids(requirements),
            [
                "FR-A-01",
                "FR-A-02",
                "FR-B-01",
                "FR-C-04",
            ]
        )

    # ---------------------------------------------------------
    # 3. DIFFERENT ID CONVENTIONS
    # ---------------------------------------------------------

    def test_different_requirement_id_conventions(self):

        requirements = self.extract(
            """
            REQ-001: The system must authenticate users.
            REQ-AUTH-002: The system must support MFA.
            R001: The system must generate invoices.
            AUTH-001: The system must lock accounts.
            """

        )

        self.assertEqual(
            len(requirements),
            4
        )

        self.assertEqual(
            self.ids(requirements),
            [
                "REQ-001",
                "REQ-AUTH-002",
                "R001",
                "AUTH-001",
            ]
        )

    # ---------------------------------------------------------
    # 4. REQUIREMENTS WITHOUT IDs
    # ---------------------------------------------------------

    def test_requirements_without_ids(self):

        requirements = self.extract(
            """
            Customers should be able to add products to their cart.

            The checkout process shall support mobile money.

            Users can view their order history.

            Customers must receive an email confirmation after payment.
            """
        )

        self.assertEqual(
            len(requirements),
            4
        )

        texts = self.texts(requirements)

        self.assertTrue(
            any(
                "add products" in text.lower()
                for text in texts
            )
        )

        self.assertTrue(
            any(
                "mobile money" in text.lower()
                for text in texts
            )
        )

    # ---------------------------------------------------------
    # 5. CAPABILITY LANGUAGE
    # ---------------------------------------------------------

    def test_capability_language_without_modal(self):

        requirements = self.extract(
            """
            Users can search for products by name.

            Customers are able to download invoices.

            The application allows users to reset passwords.
            """
        )

        self.assertEqual(
            len(requirements),
            3
        )

    # ---------------------------------------------------------
    # 6. USER STORIES
    # ---------------------------------------------------------

    def test_user_stories(self):

        requirements = self.extract(
            """
            As a customer, I want to track my order.

            As an administrator, I want to manage products.

            As a customer, I want to save products to my wishlist.
            """
        )

        self.assertEqual(
            len(requirements),
            3
        )

    # ---------------------------------------------------------
    # 7. NON-FUNCTIONAL REQUIREMENTS WITHOUT IDs
    # ---------------------------------------------------------

    def test_unnumbered_non_functional_requirements(self):

        requirements = self.extract(
            """
            Response time must remain below 2 seconds.

            The application should maintain 99.9% availability.

            All transmitted data shall use TLS 1.3.
            """
        )

        self.assertEqual(
            len(requirements),
            3
        )

    # ---------------------------------------------------------
    # 8. MULTILINE REQUIREMENTS
    # ---------------------------------------------------------

    def test_multiline_requirement(self):

        requirements = self.extract(
            """
            FR-01: The system must allow customers
            to add products to their shopping cart
            and modify the quantity before checkout.
            """
        )

        self.assertEqual(
            len(requirements),
            1
        )

        self.assertIn(
            "modify the quantity",
            requirements[0].text
        )

    # ---------------------------------------------------------
    # 9. REQUIREMENTS MIXED WITH HEADINGS
    # ---------------------------------------------------------

    def test_requirements_mixed_with_document_headings(self):

        requirements = self.extract(
            """
            3. Functional Requirements

            3.1 Authentication

            FR-01: The system must authenticate users.

            3.2 Shopping Cart

            FR-02: Customers should be able to add products
            to the shopping cart.
            """
        )

        self.assertEqual(
            len(requirements),
            2
        )

        texts = self.texts(requirements)

        self.assertFalse(
            any(
                "3.1 Authentication" in text
                for text in texts
            )
        )

        self.assertFalse(
            any(
                "3.2 Shopping Cart" in text
                for text in texts
            )
        )

    # ---------------------------------------------------------
    # 10. APPENDIX MUST NOT BECOME A REQUIREMENT
    # ---------------------------------------------------------

    def test_appendix_is_not_attached_to_final_requirement(self):

        requirements = self.extract(
            """
            NFR-01: The system must maintain 99.9% uptime.

            Appendix A: Data Dictionary

            Patient_ID | String | Primary Key
            Doctor_ID | String | Primary Key
            """
        )

        self.assertEqual(
            len(requirements),
            1
        )

        self.assertNotIn(
            "Appendix",
            requirements[0].text
        )

    # ---------------------------------------------------------
    # 11. NORMAL DOCUMENT TEXT MUST NOT BECOME REQUIREMENT
    # ---------------------------------------------------------

    def test_non_requirement_document_text(self):

        requirements = self.extract(
            """
            This document describes the proposed e-commerce platform.

            The project team will use Agile methodology.

            The application was developed using Python.

            The system must allow customers to place orders.
            """
        )

        self.assertEqual(
            len(requirements),
            1
        )

        self.assertIn(
            "place orders",
            requirements[0].text
        )

    # ---------------------------------------------------------
    # 12. DIFFERENT DOMAINS
    # ---------------------------------------------------------

    def test_ecommerce_requirements(self):

        requirements = self.extract(
            """
            Customers should be able to compare products.

            The checkout process shall support Visa and Mastercard.

            Users must receive an order confirmation after payment.
            """
        )

        self.assertEqual(
            len(requirements),
            3
        )

    def test_healthcare_requirements(self):

        requirements = self.extract(
            """
            Doctors must be able to create patient records.

            Nurses should be able to update vital signs.

            The system shall encrypt patient data at rest.
            """
        )

        self.assertEqual(
            len(requirements),
            3
        )

    def test_banking_requirements(self):

        requirements = self.extract(
            """
            Customers must be able to transfer funds.

            The system shall require MFA for transactions.

            Transaction processing must complete within 3 seconds.
            """
        )

        self.assertEqual(
            len(requirements),
            3
        )

    # ---------------------------------------------------------
    # 13. MIXED FORMATS IN ONE DOCUMENT
    # ---------------------------------------------------------

    def test_mixed_requirement_formats(self):

        requirements = self.extract(
            """
            FR-01: The system must allow registration.

            Customers should be able to browse products.

            REQ-PAY-002: The checkout process shall support mobile money.

            As a customer, I want to track my order.

            Response time must remain below 2 seconds.
            """
        )

        self.assertEqual(
            len(requirements),
            5
        )

        self.assertEqual(
            self.ids(requirements),
            [
                "FR-01",
                None,
                "REQ-PAY-002",
                None,
                None,
            ]
        )

    # ---------------------------------------------------------
    # 14. REQUIREMENTS WITH PUNCTUATION AND COLONS
    # ---------------------------------------------------------

    def test_requirement_id_punctuation(self):

        requirements = self.extract(
            """
            FR-01. The system must allow registration.
            FR-02) The system must allow login.
            FR-03 - The system must allow password reset.
            """
        )

        self.assertEqual(
            len(requirements),
            3
        )


if __name__ == "__main__":
    unittest.main()