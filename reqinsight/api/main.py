from pathlib import Path
import shutil
import tempfile
import zipfile

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

ALLOWED_CONTENT_TYPES = {
    ".pdf": {
        "application/pdf",
    },
    ".docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/zip",
        "application/octet-stream",
    },
    ".txt": {
        "text/plain",
        "application/octet-stream",
    },
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_file_content(
    file_path: Path,
    extension: str
) -> bool:

    if extension == ".pdf":

        with open(file_path, "rb") as file:
            header = file.read(5)

        return header == b"%PDF-"

    if extension == ".docx":

        if not zipfile.is_zipfile(file_path):
            return False

        try:
            with zipfile.ZipFile(file_path, "r") as archive:
                names = archive.namelist()

                return (
                    "[Content_Types].xml" in names
                    and "word/document.xml" in names
                )

        except zipfile.BadZipFile:
            return False

    if extension == ".txt":

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                file.read(4096)

            return True

        except UnicodeDecodeError:
            return False

    return False


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

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A file must be provided.",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    # ---------------------------------------------------------
    # Extension validation
    # ---------------------------------------------------------

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Supported formats: PDF, DOCX, TXT."
            ),
        )

    # ---------------------------------------------------------
    # Content-Type validation
    # ---------------------------------------------------------

    content_type = file.content_type

    allowed_types = ALLOWED_CONTENT_TYPES[
        extension
    ]

    if (
        content_type
        and content_type not in allowed_types
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid content type for "
                f"{extension} file."
            ),
        )

    temporary_path = None
    total_size = 0

    try:

        # -----------------------------------------------------
        # Temporary file
        # -----------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temporary_file:

            temporary_path = Path(
                temporary_file.name
            )

            # -------------------------------------------------
            # Stream upload and enforce size limit
            # -------------------------------------------------

            while True:

                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail=(
                            "File is too large. "
                            "Maximum allowed size is 10 MB."
                        ),
                    )

                temporary_file.write(chunk)

        # -----------------------------------------------------
        # File-content validation
        # -----------------------------------------------------

        if not validate_file_content(
            temporary_path,
            extension
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "The uploaded file does not "
                    "match its file type."
                ),
            )

        # -----------------------------------------------------
        # ReqInsight analysis
        # -----------------------------------------------------

        result = analysis_service.analyze(
            temporary_path
        )

        return build_public_response(
            result,
            Path(file.filename).name,
        )

    except HTTPException:
        raise

    except Exception:
        # Do not expose internal exception details publicly.
        raise HTTPException(
            status_code=500,
            detail=(
                "Document analysis failed. "
                "Please verify that the document is valid "
                "and try again."
            ),
        )

    finally:

        if (
            temporary_path
            and temporary_path.exists()
        ):
            temporary_path.unlink()

        await file.close()