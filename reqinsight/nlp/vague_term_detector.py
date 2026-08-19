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

        # Additional vague terminology identified during evaluation
        "clear",
        "clearly",
        "consistent",
        "detailed",
        "prominent",
        "prominently",
        "secure",
        "securely",
        "low technical proficiency",
    }

    def detect(self, text: str) -> List[str]:
        """
        Detect potentially vague terms in a requirement.

        Returns:
            A list of vague terms found in the text.
        """

        text_lower = text.lower()
        detected = []

        # "Fast" in FHIR is part of the formal expansion:
        # Fast Healthcare Interoperability Resources.
        # It should not be treated as vague terminology.
        fhir_pattern = r"\bfast\s+healthcare\s+interoperability\s+resources\b"

        fhir_match = re.search(fhir_pattern, text_lower)

        for term in self.VAGUE_TERMS:

            # Skip "fast" when it occurs as part of the
            # formal FHIR name.
            if term == "fast" and fhir_match:
                continue

            pattern = rf"\b{re.escape(term)}\b"

            if re.search(pattern, text_lower):
                detected.append(term)

        return detected