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


if __name__ == "__main__":
    unittest.main()