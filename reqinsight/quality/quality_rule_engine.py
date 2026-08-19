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

        findings.extend(
            self._check_verifiability(analysis)
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
        """Check whether a requirement contains an objective measurable criterion."""

        requirement_id = analysis.get("requirement_id", "")

        constraints = analysis.get(
            "quantifiable_constraints", []
        )

        vague_terms = analysis.get(
            "vague_terms", []
        )

        technical_criteria = analysis.get(
            "technical_criteria", []
        )

        verification_terms = analysis.get(
            "verification_terms", []
        )

        objective_indicators = analysis.get(
            "objective_indicators", []
        )

        # ---------------------------------------------------------
        # 1. Quantifiable constraints are directly measurable.
        # ---------------------------------------------------------

        if constraints:
            return []

        # ---------------------------------------------------------
        # 2. Explicit technical criteria provide an objective
        #    acceptance criterion.
        # ---------------------------------------------------------

        if technical_criteria:
            return []

        # ---------------------------------------------------------
        # 3. Explicit verification terms can make a requirement
        #    objectively testable.
        #
        #    Examples:
        #    "must be localized"
        #    "must support"
        #    "must comply"
        # ---------------------------------------------------------

        if verification_terms:
            return []

        # ---------------------------------------------------------
        # 4. Strong objective indicators can provide observable
        #    system behaviour even without a numerical constraint.
        # ---------------------------------------------------------

        strong_objective_indicators = {
            "must display",
            "must generate",
            "must send",
            "must allow",
            "must support",
            "must maintain",
            "must provide",
            "must store",
            "must validate",
            "must enforce",
            "must trigger",
            "must notify",
            "must encrypt",
            "must record",
            "must integrate",
            "shall display",
            "shall generate",
            "shall send",
            "shall allow",
            "shall support",
            "shall maintain",
            "shall provide",
            "shall store",
            "shall validate",
            "shall enforce",
            "shall trigger",
            "shall notify",
            "shall encrypt",
            "shall record",
            "shall integrate",
        }

        if any(
            indicator in strong_objective_indicators
            for indicator in objective_indicators
        ):
            return []

        # ---------------------------------------------------------
        # 5. Vague/subjective terminology without an objective
        #    criterion should produce a measurability warning
        #    for requirements in the evaluation categories.
        #
        #    However, do not automatically classify every vague
        #    requirement as a measurability problem.
        # ---------------------------------------------------------

        if vague_terms:
            measurable_vague_terms = {
                "properly",
                "appropriately",
                "appropriate",
                "suitable",
                "easy",
                "easy to use",
                "efficiently",
                "efficient",
                "reliable",
                "useful",
                "satisfactory",
                "secure handling",
                "securely",
                "secure",
                "detailed",
                "prominently",
                "consistent look and feel",
                "normal operating conditions",
                "peak usage",
                "low technical proficiency",
            }

            if any(
                term in measurable_vague_terms
                for term in vague_terms
            ):
                if (
                    requirement_id.startswith("NFR-")
                    or requirement_id.startswith("VER-")
                ):
                    return [
                        {
                            "rule": "MEASURABILITY",
                            "severity": "WARNING",
                            "message": (
                                "Requirement does not contain an "
                                "explicit measurable criterion."
                            ),
                            "recommendation": (
                                "Consider adding a measurable target, "
                                "threshold, range, limit, or objective "
                                "acceptance criterion."
                            ),
                        }
                    ]

            return []

        # ---------------------------------------------------------
        # 6. NFR and VER requirements without an objective criterion
        #    should receive a measurability warning.
        # ---------------------------------------------------------

        if (
            requirement_id.startswith("NFR-")
            or requirement_id.startswith("VER-")
        ):
            return [
                {
                    "rule": "MEASURABILITY",
                    "severity": "WARNING",
                    "message": (
                        "Requirement does not contain an explicit "
                        "measurable criterion."
                    ),
                    "recommendation": (
                        "Consider adding a measurable target, "
                        "threshold, range, limit, or objective "
                        "acceptance criterion."
                    ),
                }
            ]

        return []
    
    def _check_verifiability(self, analysis: Dict) -> List[Dict]:
        """Check whether a requirement is objectively verifiable."""

        text = analysis.get("text", "").strip()

        if not text:
            return []

        # A quantified constraint provides an objective
        # acceptance criterion and therefore makes the
        # requirement independently verifiable.
        constraints = analysis.get(
            "quantifiable_constraints", []
        )

        if constraints:
            return []

        verifiability = self.verifiability_detector.detect(text)

        if not verifiability["verifiable"]:
            return [
                {
                    "rule": "VERIFIABILITY",
                    "severity": "WARNING",
                    "message": (
                        "Requirement does not contain a clear "
                        "objectively verifiable criterion."
                    ),
                    "recommendation": (
                        "Specify observable system behavior, "
                        "a measurable condition, technical criterion, "
                        "or explicit acceptance criterion."
                    ),
                }
            ]

        return []