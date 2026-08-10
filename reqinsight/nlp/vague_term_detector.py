import re
from typing import List


class VagueTermDetector:
    """Detects potentially vague terminology in software requirements."""

    VAGUE_TERMS = {
        "easy",
        "easily",
        "fast",
        "quick",
        "quickly",
        "simple",
        "simply",
        "user-friendly",
        "appropriate",
        "adequate",
        "reasonable",
        "sufficient",
        "sufficiently",
        "efficient",
        "efficiently",
        "effective",
        "effectively",
        "reliable",
        "soon",
        "etc",
        "etc.",
        "as needed",
        "as appropriate",
        "where possible",
    }

    def detect(self, text: str) -> List[str]:
        """
        Detect potentially vague terms in a requirement.

        Returns:
            A list of vague terms found in the text.
        """

        text_lower = text.lower()
        detected = []

        for term in self.VAGUE_TERMS:

            if " " in term or "." in term or "-" in term:
                pattern = rf"\b{re.escape(term)}\b"
            else:
                pattern = rf"\b{re.escape(term)}\b"

            if re.search(pattern, text_lower):
                detected.append(term)

        return detected