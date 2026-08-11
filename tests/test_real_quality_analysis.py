import unittest
from pathlib import Path

from reqinsight.parsers.document_parser import DocumentParser
from reqinsight.analysis.requirement_extractor import RequirementExtractor
from reqinsight.nlp.requirement_analyzer import RequirementAnalyzer
from reqinsight.quality.quality_rule_engine import QualityRuleEngine
from reqinsight.quality.quality_scorer import QualityScorer
from reqinsight.quality.document_quality_scorer import (
    DocumentQualityScorer
)


class TestRealQualityAnalysis(unittest.TestCase):

    def test_analyze_real_srs(self):

        # ---------------------------------------------------------
        # 1. LOAD DOCUMENT
        # ---------------------------------------------------------

        file_path = Path("data") / "SELP_SRS.pdf"

        parser = DocumentParser()
        document = parser.parse(file_path)

        # ---------------------------------------------------------
        # 2. EXTRACT REQUIREMENTS
        # ---------------------------------------------------------

        extractor = RequirementExtractor()
        requirements = extractor.extract(document)

        # ---------------------------------------------------------
        # 3. INITIALIZE ANALYSIS COMPONENTS
        # ---------------------------------------------------------

        analyzer = RequirementAnalyzer()
        engine = QualityRuleEngine()
        scorer = QualityScorer()
        document_scorer = DocumentQualityScorer()

        # ---------------------------------------------------------
        # 4. HEADER
        # ---------------------------------------------------------

        print()
        print("=" * 60)
        print("REAL SRS QUALITY ANALYSIS TEST")
        print("=" * 60)

        print(f"Document: {file_path}")
        print(f"Requirements: {len(requirements)}")

        # ---------------------------------------------------------
        # 5. ANALYZE ALL REQUIREMENTS
        # ---------------------------------------------------------

        total_findings = 0
        quality_results = []

        for requirement in requirements:

            analysis = analyzer.analyze(requirement)

            findings = engine.evaluate(analysis)

            score_result = scorer.score(findings)

            total_findings += len(findings)

            quality_results.append({
                "requirement_id": requirement.requirement_id,
                "text": requirement.text,
                "findings": findings,
                "score": score_result["score"],
                "classification": score_result["classification"],
            })

        document_summary = document_scorer.summarize(
            quality_results
        )

        # ---------------------------------------------------------
        # 6. REQUIREMENT QUALITY SUMMARY
        # ---------------------------------------------------------

        print()
        print("REQUIREMENT QUALITY SUMMARY")
        print("-" * 60)

        for result in quality_results:

            print(
                f"{result['requirement_id']} | "
                f"{result['score']}/100 | "
                f"{result['classification']}"
            )

        # ---------------------------------------------------------
        # 7. QUALITY CLASSIFICATION SUMMARY
        # ---------------------------------------------------------

        excellent = sum(
            1
            for result in quality_results
            if result["classification"] == "EXCELLENT"
        )

        good = sum(
            1
            for result in quality_results
            if result["classification"] == "GOOD"
        )

        needs_review = sum(
            1
            for result in quality_results
            if result["classification"] == "NEEDS REVIEW"
        )

        poor = sum(
            1
            for result in quality_results
            if result["classification"] == "POOR"
        )

        print()
        print("QUALITY SUMMARY")
        print("-" * 60)

        print(f"Total Requirements: {len(quality_results)}")
        print(f"Excellent:          {excellent}")
        print(f"Good:               {good}")
        print(f"Needs Review:       {needs_review}")
        print(f"Poor:               {poor}")
        print(f"Total Findings:     {total_findings}")

        print()
        print("DOCUMENT QUALITY SCORE")
        print("-" * 60)

        print(
            f"Overall Score: "
            f"{document_summary['score']}/100"
        )

        print(
            f"Classification: "
            f"{document_summary['classification']}"
        )

        # ---------------------------------------------------------
        # 8. DETAILED FINDINGS
        # ---------------------------------------------------------

        print()
        print("DETAILED FINDINGS")
        print("-" * 60)

        for result in quality_results:

            if not result["findings"]:
                continue

            print()
            print(
                f"{result['requirement_id']}: "
                f"{result['text']}"
            )

            print(
                f"Quality Score: "
                f"{result['score']}/100 "
                f"({result['classification']})"
            )

            for finding in result["findings"]:

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
        # 9. TEST ASSERTIONS
        # ---------------------------------------------------------

        self.assertEqual(len(requirements), 39)

        self.assertEqual(
            len(quality_results),
            39
        )


if __name__ == "__main__":
    unittest.main()