from pathlib import Path

from reqinsight.parsers.document_parser import DocumentParser
from reqinsight.analysis.requirement_extractor import RequirementExtractor
from reqinsight.nlp.requirement_analyzer import RequirementAnalyzer
from reqinsight.quality.quality_rule_engine import QualityRuleEngine
from reqinsight.quality.quality_scorer import QualityScorer
from reqinsight.quality.document_quality_scorer import (
    DocumentQualityScorer
)


class RequirementAnalysisService:
    """
    Application service responsible for running the complete
    ReqInsight SRS analysis pipeline.
    """

    def __init__(self):
        self.parser = DocumentParser()
        self.extractor = RequirementExtractor()
        self.analyzer = RequirementAnalyzer()
        self.rule_engine = QualityRuleEngine()
        self.quality_scorer = QualityScorer()
        self.document_scorer = DocumentQualityScorer()

    def analyze(self, file_path):
        """
        Analyze an SRS document and return a complete quality report.
        """

        file_path = Path(file_path)

        # ---------------------------------------------------------
        # 1. Parse document
        # ---------------------------------------------------------

        document = self.parser.parse(file_path)

        # ---------------------------------------------------------
        # 2. Extract requirements
        # ---------------------------------------------------------

        requirements = self.extractor.extract(document)

        # ---------------------------------------------------------
        # 3. Analyze each requirement
        # ---------------------------------------------------------

        requirement_results = []

        for requirement in requirements:

            analysis = self.analyzer.analyze(requirement)

            findings = self.rule_engine.evaluate(analysis)

            score_result = self.quality_scorer.score(findings)

            requirement_results.append({
                "requirement_id": requirement.requirement_id,
                "text": requirement.text,
                "analysis": analysis,
                "findings": findings,
                "score": score_result["score"],
                "classification": score_result["classification"],
            })

        # ---------------------------------------------------------
        # 4. Calculate document-level quality
        # ---------------------------------------------------------

        document_summary = self.document_scorer.summarize(
            requirement_results
        )

        # ---------------------------------------------------------
        # 5. Return complete analysis result
        # ---------------------------------------------------------

        return {
            "document": {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "requirement_count": len(requirements),
            },
            "requirements": requirement_results,
            "summary": document_summary,
        }