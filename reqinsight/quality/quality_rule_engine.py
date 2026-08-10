from typing import Dict, List


class QualityRuleEngine:
    """
    Evaluates software requirements against basic
    requirement-quality rules.
    """

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

    def _check_measurability(self, analysis: Dict) -> List[Dict]:
        """Check whether a requirement contains measurable constraints."""

        requirement_id = analysis.get("requirement_id", "")
        constraints = analysis.get(
            "quantifiable_constraints", []
        )

        # For NFRs, measurable constraints are especially important.
        if requirement_id.startswith("NFR-") and not constraints:
            return [
                {
                    "rule": "MEASURABILITY",
                    "severity": "WARNING",
                    "message": (
                        "Non-functional requirement does not contain "
                        "an explicit measurable constraint."
                    ),
                    "recommendation": (
                        "Consider adding a measurable target, "
                        "threshold, limit, or acceptance criterion."
                    ),
                }
            ]

        return []