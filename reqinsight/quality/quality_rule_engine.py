from typing import Dict, List

from reqinsight.analysis.verifiability_detector import VerifiabilityDetector


class QualityRuleEngine:
    """
    Evaluates software requirements against basic
    requirement-quality rules.
    """

    def __init__(self):
        self.verifiability_detector = VerifiabilityDetector()

    def evaluate(self, analysis: Dict) -> List[Dict]:
        """
        Evaluate one analyzed requirement.

        Returns:
            A list of quality findings.
        """

        findings = []

        findings.extend(
            self._check_modal_consistency(analysis)
        )

        findings.extend(
            self._check_vague_terms(analysis)
        )

        findings.extend(
            self._check_measurability(analysis)
        )

        return findings

    def _check_modal_consistency(self, analysis: Dict) -> List[Dict]:
        """Check whether the requirement uses a weak modal."""

        modal_words = analysis.get("modal_words", [])

        if "should" in modal_words:
            return [
                {
                    "rule": "MODAL-CONSISTENCY",
                    "severity": "WARNING",
                    "message": (
                        "Requirement uses 'should', which may "
                        "indicate optional or non-mandatory behavior."
                    ),
                    "recommendation": (
                        "Confirm whether the requirement is intended "
                        "to be mandatory."
                    ),
                }
            ]

        return []

    def _check_vague_terms(self, analysis: Dict) -> List[Dict]:
        """Check for potentially vague terminology."""

        vague_terms = analysis.get("vague_terms", [])

        if vague_terms:
            return [
                {
                    "rule": "VAGUE-TERM",
                    "severity": "WARNING",
                    "message": (
                        "Potentially vague terminology detected: "
                        + ", ".join(vague_terms)
                    ),
                    "recommendation": (
                        "Replace vague terminology with specific "
                        "and objectively verifiable wording."
                    ),
                }
            ]

        return []

    def _check_measurability(self, analysis):
        """Check whether a requirement contains measurable or
        otherwise verifiable criteria."""

        requirement_id = analysis.get("requirement_id", "")

        constraints = analysis.get(
            "quantifiable_constraints", []
        )

        text = analysis.get("text", "")

        verifiability = self.verifiability_detector.detect(text)

        # Quantitative constraints make the requirement measurable.
        if constraints:
            return []

        # Technical criteria or explicit verification indicators
        # make the requirement objectively verifiable.
        if verifiability["verifiable"]:
            return []

        # Apply this rule primarily to non-functional requirements.
        if requirement_id.startswith("NFR-"):
            return [
                {
                    "rule": "MEASURABILITY",
                    "severity": "WARNING",
                    "message": (
                        "Non-functional requirement does not contain "
                        "an explicit measurable or verifiable criterion."
                    ),
                    "recommendation": (
                        "Consider adding a measurable target, "
                        "threshold, technical criterion, or "
                        "acceptance criterion."
                    ),
                }
            ]

        return []