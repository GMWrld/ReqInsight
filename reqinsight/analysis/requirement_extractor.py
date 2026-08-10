import re
from typing import List, Optional

from reqinsight.models.document import Document
from reqinsight.models.requirement import Requirement


class RequirementExtractor:
    """Extracts and reconstructs candidate requirements from SRS text."""

    REQUIREMENT_ID_PATTERN = re.compile(
        r"^\s*(?P<id>[A-Za-z]{2,10}[-_]\d{1,5})\s*[:.)-]?\s*(?P<text>.+)$"
    )

    MODAL_PATTERN = re.compile(
        r"\b(shall|must|should|may)\b",
        re.IGNORECASE
    )

    REQUIREMENT_STARTERS = (
        "the system",
        "the application",
        "the platform",
        "the software",
        "the service",
        "the user",
        "users",
        "user",
        "administrator",
        "administrators",
        "educators",
        "students",
        "the administrator",
    )

    def extract(self, document: Document) -> List[Requirement]:
        """
        Extract complete requirement statements from a parsed document.
        """

        lines = [
            self._clean_line(line)
            for line in document.text.splitlines()
        ]

        lines = [line for line in lines if line]

        requirements = []
        current_id: Optional[str] = None
        current_text: List[str] = []

        for line in lines:

            identifier_match = self.REQUIREMENT_ID_PATTERN.match(line)

            if identifier_match:
                # Save the previous requirement first.
                if current_text:
                    requirement = self._build_requirement(
                        current_id,
                        current_text
                    )

                    if requirement:
                        requirements.append(requirement)

                current_id = identifier_match.group("id")
                current_text = [
                    identifier_match.group("text").strip()
                ]

                continue

            # If we already started an identified requirement,
            # this line may be a continuation of it.
            if current_id is not None:
                if self._is_structural_heading(line):
                    requirement = self._build_requirement(
                        current_id,
                        current_text
                    )

                    if requirement:
                        requirements.append(requirement)

                    current_id = None
                    current_text = []

                    continue

                current_text.append(line)
                continue

            # Handle requirements without explicit identifiers.
            if self._contains_modal(line) and self._looks_like_requirement(line):
                requirement = Requirement(
                    requirement_id=None,
                    text=line
                )

                requirements.append(requirement)

        # Save final requirement.
        if current_text:
            requirement = self._build_requirement(
                current_id,
                current_text
            )

            if requirement:
                requirements.append(requirement)

        return requirements

    def _build_requirement(
        self,
        requirement_id: Optional[str],
        text_parts: List[str]
    ) -> Optional[Requirement]:
        """Build one complete Requirement from reconstructed text."""

        text = " ".join(text_parts)

        text = self._normalize_text(text)

        text = self._remove_embedded_structural_heading(text)

        if not self._contains_modal(text):
            return None

        return Requirement(
            requirement_id=requirement_id,
            text=text
        )

    def _contains_modal(self, text: str) -> bool:
        """Check whether text contains requirement-oriented modal language."""

        return bool(self.MODAL_PATTERN.search(text))

    def _looks_like_requirement(self, text: str) -> bool:
        """Determine whether an unnumbered statement looks like a requirement."""

        text_lower = text.lower()

        return text_lower.startswith(self.REQUIREMENT_STARTERS)

    @staticmethod
    def _clean_line(line: str) -> str:
        """Remove common extraction artifacts."""

        line = line.strip()

        # Remove common bullet characters.
        line = re.sub(r"^[•▪◦‣]\s*", "", line)

        # Normalize repeated whitespace.
        line = re.sub(r"\s+", " ", line)

        return line

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize reconstructed requirement text."""

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _is_structural_heading(self, text: str) -> bool:
        """Determine whether a line represents an SRS structural heading."""

        heading_pattern = re.compile(
            r"^\d+(?:\.\d+){0,3}\s+.+$"
        )

        if heading_pattern.match(text):
            return True

        if text.lower() in {
            "appendices",
            "appendix",
            "table of contents",
        }:
            return True

        if text.lower().startswith("appendix "):
            return True

        return False

    def _remove_embedded_structural_heading(self, text: str) -> str:
        """
        Remove structural headings that have been extracted on the
        same line as a requirement.
        """

        # Matches headings such as:
        # 3.1.2 Course Management (Educator)
        # 3.1.3 Content Consumption (Student)
        # 3.2 External Interface Requirements
        # 3.3.5 Reliability
        heading_pattern = re.compile(
            r"\s+\d+\.\d+(?:\.\d+){0,2}\s+[A-Z][^\n]*$"
        )

        text = heading_pattern.sub("", text)

        # Matches:
        # Appendices
        # Appendix A: Database Schema Diagram
        appendix_pattern = re.compile(
            r"\s+(Appendices|Appendix\s+[A-Z]\s*:)[^\n]*$",
            re.IGNORECASE
        )

        text = appendix_pattern.sub("", text)

        return text.strip()