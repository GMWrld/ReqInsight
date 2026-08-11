import sys
from pathlib import Path

from reqinsight.application.analysis_service import (
    RequirementAnalysisService
)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def print_header() -> None:
    print("=" * 60)
    print("                 ReqInsight v1.0")
    print("        Software Requirements Quality Analyzer")
    print("=" * 60)
    print()


def print_summary(result: dict, file_path: Path) -> None:
    summary = result["summary"]

    print("=" * 60)
    print("DOCUMENT QUALITY ANALYSIS")
    print("=" * 60)

    print(f"Document: {file_path.name}")
    print(f"Requirements: {summary['total_requirements']}")
    print()

    print(f"Overall Score: {summary['score']:.2f}/100")
    print(f"Classification: {summary['classification']}")
    print()

    print("Quality Distribution")
    print("-" * 60)
    print(f"Excellent:          {summary['excellent']}")
    print(f"Good:               {summary['good']}")
    print(f"Needs Review:       {summary['needs_review']}")
    print(f"Poor:               {summary['poor']}")
    print()


def print_findings(result: dict) -> None:
    findings_found = False

    print("=" * 60)
    print("QUALITY FINDINGS")
    print("=" * 60)

    for requirement in result["requirements"]:
        findings = requirement.get("findings", [])

        if not findings:
            continue

        findings_found = True

        print()
        print(
            f"{requirement['requirement_id']}: "
            f"{requirement['text']}"
        )
        print(
            f"Quality Score: "
            f"{requirement['score']:.0f}/100 "
            f"({requirement['classification']})"
        )

        for finding in findings:
            print(
                f"[{finding['severity']}] "
                f"{finding['rule']}"
            )
            print(
                f"Message: "
                f"{finding['message']}"
            )
            print(
                f"Recommendation: "
                f"{finding['recommendation']}"
            )

    if not findings_found:
        print()
        print("No quality findings detected.")

    print()


def analyze_file(file_path: Path) -> int:
    if not file_path.exists():
        print(
            f"ERROR: File not found: {file_path}"
        )
        return 1

    if not file_path.is_file():
        print(
            f"ERROR: Path is not a file: {file_path}"
        )
        return 1

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print(
            "ERROR: Unsupported file type."
        )
        print(
            "Supported formats: PDF, DOCX, TXT"
        )
        return 1

    print(f"Analyzing: {file_path}")
    print()

    try:
        service = RequirementAnalysisService()

        result = service.analyze(file_path)

        print_summary(
            result,
            file_path
        )

        print_findings(result)

        print("=" * 60)
        print("Analysis completed successfully.")
        print("=" * 60)

        return 0

    except Exception as exc:
        print(
            f"ERROR: Analysis failed: {exc}"
        )
        return 1


def main() -> None:
    print_header()

    if len(sys.argv) != 2:
        print(
            "Usage:"
        )
        print(
            "  python main.py <path-to-srs-document>"
        )
        print()
        print(
            "Example:"
        )
        print(
            r"  python main.py data\SELP_SRS.pdf"
        )
        return

    file_path = Path(sys.argv[1])

    exit_code = analyze_file(file_path)

    if exit_code != 0:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()