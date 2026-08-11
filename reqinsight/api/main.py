from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile

from reqinsight.application.analysis_service import (
    RequirementAnalysisService
)


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


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ReqInsight API",
    }


@app.post("/api/analyze")
async def analyze_document(
    file: UploadFile = File(...)
):
    """
    Analyze an uploaded SRS document.

    Supported formats:
    PDF, DOCX, TXT
    """

    # ---------------------------------------------------------
    # 1. Validate filename
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # 2. Create temporary file
    # ---------------------------------------------------------

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

        # -----------------------------------------------------
        # 3. Run ReqInsight analysis
        # -----------------------------------------------------

        result = analysis_service.analyze(
            temporary_path
        )

        # Preserve the user's original filename
        result["document"]["file_name"] = file.filename

        return result

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Document analysis failed: {str(exc)}",
        )

    finally:

        # -----------------------------------------------------
        # 4. Delete temporary file
        # -----------------------------------------------------

        if temporary_path and temporary_path.exists():
            temporary_path.unlink()