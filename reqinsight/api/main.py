from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile

from reqinsight.application.analysis_service import (
    RequirementAnalysisService
)

from reqinsight.api.schemas import AnalysisResponse


app = FastAPI(
    title="ReqInsight API",
    description="REST API for SRS quality analysis",
    version="1.0.0",
)


analysis_service = RequirementAnalysisService()


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def build_public_response(
    result: dict,
    original_filename: str
) -> dict:

    requirements = []

    for requirement in result["requirements"]:

        findings = []

        for finding in requirement.get("findings", []):

            findings.append({
                "rule": finding["rule"],
                "severity": finding["severity"],
                "message": finding["message"],
                "recommendation": finding["recommendation"],
            })

        requirements.append({
            "id": requirement["requirement_id"],
            "text": requirement["text"],
            "score": requirement["score"],
            "classification": requirement["classification"],
            "findings": findings,
        })

    summary = result["summary"]

    return {
        "document": {
            "file_name": original_filename,
            "requirement_count": summary["total_requirements"],
        },
        "summary": {
            "score": summary["score"],
            "classification": summary["classification"],
            "total_requirements": summary["total_requirements"],
            "excellent": summary["excellent"],
            "good": summary["good"],
            "needs_review": summary["needs_review"],
            "poor": summary["poor"],
        },
        "requirements": requirements,
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ReqInsight API",
    }


@app.post(
    "/api/analyze",
    response_model=AnalysisResponse
)
async def analyze_document(
    file: UploadFile = File(...)
):
    """
    Analyze an uploaded SRS document.

    Supported formats:
    PDF, DOCX, TXT
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A file must be provided.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Supported formats: PDF, DOCX, TXT."
            ),
        )

    temporary_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temporary_file:

            temporary_path = Path(
                temporary_file.name
            )

            shutil.copyfileobj(
                file.file,
                temporary_file,
            )

        result = analysis_service.analyze(
            temporary_path
        )

        return build_public_response(
            result,
            file.filename,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Document analysis failed: {str(exc)}",
        )

    finally:

        if temporary_path and temporary_path.exists():
            temporary_path.unlink()