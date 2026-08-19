import re
from typing import List


class QuantifiableConstraintDetector:
    """Detects measurable constraints in software requirements."""

    PATTERNS = [
        # Percentages
        r"\b\d+(?:\.\d+)?\s*%",

        # Time in milliseconds
        r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:ms|milliseconds?)\b",

        # Time durations
        r"\b\d+(?:,\d{3})*(?:\.\d+)?(?:\s+|-)(?:s|sec|secs|seconds?|m|min|mins|minutes?|h|hr|hrs|hours?|d|day|days?|y|yr|yrs|years?)\b",

        # Quantities with countable entities
        r"\b\d+(?:,\d{3})*(?:\.\d+)?(?:\s+(?:concurrent|active|total|maximum|minimum))?\s*(?:users?|requests?|items?|records?|devices?|transactions?|sessions?)\b",

        # Quantity followed by a unit such as MB / GB
        r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:kb|mb|gb|tb)\b",

        # "within X seconds/minutes/hours"
        r"\bwithin\s+\d+(?:,\d{3})*(?:\.\d+)?\s*(?:ms|milliseconds?|s|sec|secs|seconds?|m|min|mins|minutes?|h|hr|hrs|hours?)\b",

        # "up to X MB/GB/etc."
        r"\bup\s+to\s+\d+(?:,\d{3})*(?:\.\d+)?\s*(?:kb|mb|gb|tb)\b",

        # "at least / at most X ..."
        r"\b(?:at\s+least|at\s+most)\s+\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:%|ms|milliseconds?|s|sec|secs|seconds?|m|min|mins|minutes?|h|hr|hrs|hours?|kb|mb|gb|tb))?\b",

        # "every X seconds/minutes/hours/days"
        r"\bevery\s+\d+(?:,\d{3})*(?:\.\d+)?\s*(?:ms|milliseconds?|s|sec|secs|seconds?|m|min|mins|minutes?|h|hr|hrs|hours?|d|day|days?)\b",
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