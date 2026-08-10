import unittest

from reqinsight.parsers.document_parser import DocumentParser
from reqinsight.analysis.requirement_extractor import RequirementExtractor
from reqinsight.nlp.requirement_analyzer import RequirementAnalyzer
from reqinsight.quality.quality_rule_engine import QualityRuleEngine
from pathlib import Path


class TestRealQualityAnalysis(unittest.TestCase):

    def test_analyze_real_srs(self):

        file_path = Path("data") / "SELP_SRS.pdf"

        parser = DocumentParser()
        document = parser.parse(file_path)

        extractor = RequirementExtractor()
        requirements = extractor.extract(document)

        analyzer = RequirementAnalyzer()
        engine = QualityRuleEngine()

        print()
        print("=" * 40)
        print("REAL SRS QUALITY ANALYSIS TEST")
        print("=" * 40)
        print(f"Document: {file_path}")
        print(f"Requirements: {len(requirements)}")
        print()
        print("QUALITY FINDINGS")
        print("-" * 40)

        total_findings = 0

        for requirement in requirements:

            analysis = analyzer.analyze(requirement)

            findings = engine.evaluate(analysis)

            total_findings += len(findings)

            if findings:

                print()
                print(
                    f"{requirement.requirement_id}: "
                    f"{requirement.text}"
                )

                for finding in findings:

                    print(
                        f"  [{finding['severity']}] "
                        f"{finding['rule']}"
                    )

                    print(
                        f"  {finding['message']}"
                    )

                    print(
                        f"  Recommendation: "
                        f"{finding['recommendation']}"
                    )

        print()
        print("-" * 40)
        print(f"Total findings: {total_findings}")

        self.assertEqual(len(requirements), 39)


if __name__ == "__main__":
    unittest.main()