import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from reqinsight.api.main import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

        self.pdf_path = (
            Path("data") / "SELP_SRS.pdf"
        )

        self.docx_path = (
            Path("data") / "SELP_SRS.docx"
        )

    def test_health_check(self):

        response = self.client.get(
            "/api/health"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json(),
            {
                "status": "healthy",
                "service": "ReqInsight API",
            }
        )

    def test_analyze_pdf(self):

        with open(
            self.pdf_path,
            "rb"
        ) as file:

            response = self.client.post(
                "/api/analyze",
                files={
                    "file": (
                        "SELP_SRS.pdf",
                        file,
                        "application/pdf",
                    )
                },
            )

        self.assertEqual(
            response.status_code,
            200
        )

        result = response.json()

        self.assertEqual(
            result["document"]["file_name"],
            "SELP_SRS.pdf"
        )

        self.assertEqual(
            result["document"]["requirement_count"],
            39
        )

        self.assertEqual(
            result["summary"]["score"],
            99.23
        )

        self.assertEqual(
            result["summary"]["classification"],
            "EXCELLENT"
        )

        self.assertEqual(
            len(result["requirements"]),
            39
        )

    def test_analyze_docx(self):

        with open(
            self.docx_path,
            "rb"
        ) as file:

            response = self.client.post(
                "/api/analyze",
                files={
                    "file": (
                        "SELP_SRS.docx",
                        file,
                        (
                            "application/"
                            "vnd.openxmlformats-officedocument."
                            "wordprocessingml.document"
                        ),
                    )
                },
            )

        self.assertEqual(
            response.status_code,
            200
        )

        result = response.json()

        self.assertEqual(
            result["document"]["file_name"],
            "SELP_SRS.docx"
        )

        self.assertEqual(
            result["document"]["requirement_count"],
            39
        )

        self.assertEqual(
            result["summary"]["classification"],
            "EXCELLENT"
        )

    def test_public_response_does_not_expose_internal_analysis(
        self
    ):

        with open(
            self.pdf_path,
            "rb"
        ) as file:

            response = self.client.post(
                "/api/analyze",
                files={
                    "file": (
                        "SELP_SRS.pdf",
                        file,
                        "application/pdf",
                    )
                },
            )

        self.assertEqual(
            response.status_code,
            200
        )

        result = response.json()

        # Internal NLP analysis should not be exposed.
        self.assertNotIn(
            "analysis",
            result["requirements"][0]
        )

        # Temporary server paths should not be exposed.
        self.assertNotIn(
            "file_path",
            result["document"]
        )

    def test_requirement_contains_public_fields(
        self
    ):

        with open(
            self.pdf_path,
            "rb"
        ) as file:

            response = self.client.post(
                "/api/analyze",
                files={
                    "file": (
                        "SELP_SRS.pdf",
                        file,
                        "application/pdf",
                    )
                },
            )

        self.assertEqual(
            response.status_code,
            200
        )

        requirement = response.json()["requirements"][0]

        expected_fields = {
            "id",
            "text",
            "score",
            "classification",
            "findings",
        }

        self.assertEqual(
            set(requirement.keys()),
            expected_fields
        )

    def test_reject_unsupported_file_type(self):

        response = self.client.post(
            "/api/analyze",
            files={
                "file": (
                    "test.exe",
                    b"not a supported document",
                    "application/octet-stream",
                )
            },
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "Unsupported file type",
            response.json()["detail"]
        )

    def test_analyze_requires_file(self):

        response = self.client.post(
            "/api/analyze"
        )

        self.assertEqual(
            response.status_code,
            422
        )

    def test_reject_oversized_file(self):

        oversized_content = b"x" * (
            10 * 1024 * 1024 + 1
        )

        response = self.client.post(
            "/api/analyze",
            files={
                "file": (
                    "large.txt",
                    oversized_content,
                    "text/plain",
                )
            },
        )

        self.assertEqual(
            response.status_code,
            413
        )

        self.assertIn(
            "File is too large",
            response.json()["detail"]
        )


    def test_reject_invalid_pdf_content(self):

        response = self.client.post(
            "/api/analyze",
            files={
                "file": (
                    "fake.pdf",
                    b"This is not actually a PDF.",
                    "application/pdf",
                )
            },
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "does not match its file type",
            response.json()["detail"]
        )


    def test_reject_invalid_docx_content(self):

        response = self.client.post(
            "/api/analyze",
            files={
                "file": (
                    "fake.docx",
                    b"This is not actually a DOCX.",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "does not match its file type",
            response.json()["detail"]
        )


if __name__ == "__main__":
    unittest.main()