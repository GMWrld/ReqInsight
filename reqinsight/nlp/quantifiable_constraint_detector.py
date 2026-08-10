import re
from typing import List


class QuantifiableConstraintDetector:
    """Detects measurable constraints in software requirements."""

    PATTERNS = [
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:ms|milliseconds?)\b",
        r"\b\d+(?:\.\d+)?\s*(?:s|sec|secs|seconds?)\b",
        r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:users?|requests?|items?|records?)\b",
    ]

    def detect(self, text: str) -> List[str]:
        """
        Detect measurable constraints in a requirement.

        Returns:
            A list of measurable expressions found in the text.
        """

        detected = []

        for pattern in self.PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)

            for match in matches:
                if match not in detected:
                    detected.append(match)

        # Remove standalone numbers that are already part of
        # a percentage or unit-based measurement.
        cleaned = []

        for value in detected:

            if re.fullmatch(r"\d+(?:\.\d+)?", value):
                continue

            if value not in cleaned:
                cleaned.append(value)

        return cleaned