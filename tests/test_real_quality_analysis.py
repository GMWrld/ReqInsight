import unittest
from pathlib import Path

from reqinsight.application.analysis_service import (
    RequirementAnalysisService
)


class TestRealQualityAnalysis(unittest.TestCase):

    def test_analyze_real_srs(self):

        # ---------------------------------------------------------
        # 1. LOAD ANALYSIS SERVICE
        # ---------------------------------------------------------

        service = RequirementAnalysisService()

        file_path = Path("data") / "SELP_SRS.pdf"

        # ---------------------------------------------------------
        # 2. RUN COMPLETE ANALYSIS
        # ---------------------------------------------------------

        result = service.analyze(file_path)

        requirements = result["requirements"]
        summary = result["summary"]

        # ---------------------------------------------------------
        # 3. HEADER
        # ---------------------------------------------------------

        print()
        print("=" * 60)
        print("REAL SRS QUALITY ANALYSIS TEST")
        print("=" * 60)

        print(
            f"Document: {result['document']['file_path']}"
        )

        print(
            f"Requirements: "
            f"{result['document']['requirement_count']}"
        )

        # ---------------------------------------------------------
        # 4. REQUIREMENT QUALITY SUMMARY
        # ---------------------------------------------------------

        print()
        print("REQUIREMENT QUALITY SUMMARY")
        print("-" * 60)

        for requirement in requirements:

            print(
                f"{requirement['requirement_id']} | "
                f"{requirement['score']}/100 | "
                f"{requirement['classification']}"
            )

        # ---------------------------------------------------------
        # 5. QUALITY SUMMARY
        # ---------------------------------------------------------

        print()
        print("QUALITY SUMMARY")
        print("-" * 60)

        print(
            f"Total Requirements: "
            f"{summary['total_requirements']}"
        )

        print(
            f"Excellent:          "
            f"{summary['excellent']}"
        )

        print(
            f"Good:               "
            f"{summary['good']}"
        )

        print(
            f"Needs Review:       "
            f"{summary['needs_review']}"
        )

        print(
            f"Poor:               "
            f"{summary['poor']}"
        )

        total_findings = sum(
            len(requirement["findings"])
            for requirement in requirements
        )

        print(
            f"Total Findings:     "
            f"{total_findings}"
        )

        # ---------------------------------------------------------
        # 6. DOCUMENT QUALITY SCORE
        # ---------------------------------------------------------

        print()
        print("DOCUMENT QUALITY SCORE")
        print("-" * 60)

        print(
            f"Overall Score: "
            f"{summary['score']}/100"
        )

        print(
            f"Classification: "
            f"{summary['classification']}"
        )

        # ---------------------------------------------------------
        # 7. DETAILED FINDINGS
        # ---------------------------------------------------------

        print()
        print("DETAILED FINDINGS")
        print("-" * 60)

        for requirement in requirements:

            if not requirement["findings"]:
                continue

            print()

            print(
                f"{requirement['requirement_id']}: "
                f"{requirement['text']}"
            )

            print(
                f"Quality Score: "
                f"{requirement['score']}/100 "
                f"({requirement['classification']})"
            )

            for finding in requirement["findings"]:

                print(
                    f"[{finding['severity']}] "
                    f"{finding['rule']}"
                )

                print(
                    f"{finding['message']}"
                )

                print(
                    f"Recommendation: "
                    f"{finding['recommendation']}"
                )

        # ---------------------------------------------------------
        # 8. TEST ASSERTIONS
        # ---------------------------------------------------------

        self.assertEqual(
            result["document"]["requirement_count"],
            39
        )

        self.assertEqual(
            len(requirements),
            39
        )

        self.assertEqual(
            summary["excellent"],
            37
        )

        self.assertEqual(
            summary["good"],
            2
        )

        self.assertEqual(
            summary["needs_review"],
            0
        )

        self.assertEqual(
            summary["poor"],
            0
        )

        self.assertEqual(
            summary["score"],
            99.23
        )

        self.assertEqual(
            summary["classification"],
            "EXCELLENT"
        )

        self.assertEqual(
            total_findings,
            2
        )


if __name__ == "__main__":
    unittest.main()