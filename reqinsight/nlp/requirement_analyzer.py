import re
from typing import Dict

from reqinsight.models.requirement import Requirement
from reqinsight.nlp.vague_term_detector import VagueTermDetector

from reqinsight.nlp.quantifiable_constraint_detector import (
    QuantifiableConstraintDetector
)


class RequirementAnalyzer:
    """Performs NLP analysis on software requirements."""

    MODAL_WORDS = {
        "shall",
        "must",
        "should",
        "may",
        "will",
        "can",
    }

    def __init__(self):
        self.vague_term_detector = VagueTermDetector()
        self.quantifiable_constraint_detector = (
            QuantifiableConstraintDetector()
        )

    def analyze(self, requirement: Requirement) -> Dict:
        """
        Analyze one software requirement and return linguistic features.
        """

        text = requirement.text.strip()

        words = self._tokenize(text)

        vague_terms = self.vague_term_detector.detect(text)

        quantifiable_constraints = (
            self.quantifiable_constraint_detector.detect(text)
        )

        return {
            "requirement_id": requirement.requirement_id,
            "text": text,
            "word_count": len(words),
            "character_count": len(text),
            "modal_words": self._find_modal_words(words),
            "has_modal": self._has_modal_words(words),
            "vague_terms": vague_terms,
            "has_vague_terms": len(vague_terms) > 0,
            "quantifiable_constraints": quantifiable_constraints,
            "has_quantifiable_constraint": len(quantifiable_constraints) > 0,
        }

    def _tokenize(self, text: str):
        """Tokenize requirement text into words."""

        return re.findall(r"\b[\w'-]+\b", text.lower())

    def _find_modal_words(self, words):
        """Return requirement-oriented modal words found in the text."""

        return [
            word
            for word in words
            if word in self.MODAL_WORDS
        ]

    def _has_modal_words(self, words):
        """Determine whether the requirement contains a modal word."""

        return any(
            word in self.MODAL_WORDS
            for word in words
        )

    def test_detect_quantifiable_constraints(self):

        requirement = Requirement(
            requirement_id="NFR-01",
            text=(
                "The platform must support up to 1,000 concurrent users "
                "with a response time under 2 seconds."
            )
        )

        result = self.analyzer.analyze(requirement)

        self.assertIn(
            "1,000 users",
            result["quantifiable_constraints"]
        )

        self.assertIn(
            "2 seconds",
            result["quantifiable_constraints"]
        )

        self.assertTrue(
            result["has_quantifiable_constraint"]
        )