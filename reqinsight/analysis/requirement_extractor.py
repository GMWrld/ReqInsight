import re
from typing import List, Optional

from reqinsight.models.document import Document
from reqinsight.models.requirement import Requirement

from reqinsight.analysis.requirement_candidate_detector import (
    RequirementCandidateDetector,
)


class RequirementExtractor:
    """
    Extracts and reconstructs software requirements from document text.

    The extractor is domain-agnostic. It does not assume a particular
    requirement ID prefix such as FR/NFR, nor does it depend on a
    particular application domain.
    """

    candidate_detector = RequirementCandidateDetector()

    REQUIREMENT_ID_PATTERN = re.compile(
        r"^\s*"
        r"(?P<id>"
        r"[A-Za-z]{1,12}"
        r"(?:[-_][A-Za-z0-9]{1,20})*"
        r"\d{1,6}"
        r")"
        r"\s*[:.)-]?\s*"
        r"(?P<text>.+)$"
    )

    MODAL_PATTERN = re.compile(
        r"\b(shall|must|should|may)\b",
        re.IGNORECASE,
    )

    # Generic subject starters only.
    REQUIREMENT_STARTERS = (
        "the system",
        "the application",
        "the platform",
        "the software",
        "the service",
        "the interface",
        "the portal",
        "the website",
        "the backend",
        "the frontend",
        "the database",
        "the mobile application",
        "the web application",
        "the user",
        "users",
        "user",
        "customers",
        "customer",
        "clients",
        "client",
        "administrators",
        "administrator",
        "operators",
        "operator",
        "staff",
        "employees",
        "employee",
        "all ",
    )

    # IDs that are clearly document metadata rather than requirements.
    DOCUMENT_ID_CONTEXT_PATTERN = re.compile(
        r"^\s*(?:"
        r"document\s+(?:number|id|identifier|code)\b|"
        r"doc(?:ument)?\s*[:#-]\s*|"
        r"file\s+(?:number|id|name)\b|"
        r"revision\s*(?:number|id)?\s*[:#-]\s*|"
        r"version\s*(?:number|id)?\s*[:#-]\s*"
        r")",
        re.IGNORECASE,
    )

    # Agile/backlog metadata.
    PRIORITY_PATTERN = re.compile(
        r"^\s*(?:high|medium|low)\s*"
        r"\((?:must|should|could|won't|wont)\)\s*$",
        re.IGNORECASE,
    )

    # Standalone table headers.
    TABLE_HEADER_PATTERN = re.compile(
        r"^\s*(?:"
        r"story\s+id|"
        r"user\s+story|"
        r"priority|"
        r"acceptance\s+criteria|"
        r"category|"
        r"requirement|"
        r"requirement\s+id|"
        r"detail|"
        r"specification|"
        r"guideline\s+id"
        r")\s*$",
        re.IGNORECASE,
    )

    # Common headings that may be embedded after a requirement.
    MODULE_HEADING_PATTERN = re.compile(
        r"\s+(?:module|section|chapter)\s+"
        r"\d+(?::|\s+)[^:]*$",
        re.IGNORECASE,
    )

    NUMBERED_SECTION_PATTERN = re.compile(
        r"^\s*\d+(?:\.\d+)*\s+.+$",
        re.IGNORECASE,
    )

    NON_REQUIREMENT_SECTION_PATTERN = re.compile(
        r"^\s*\d+(?:\.\d+)*\s+"
        r"(?:"
        r"assumptions?|"
        r"dependencies?|"
        r"appendix|"
        r"appendixes|"
        r"appendices|"
        r"references?"
        r")\b.*$",
        re.IGNORECASE,
    )

    def extract(self, document: Document) -> List[Requirement]:
        """
        Extract complete requirement statements from a parsed document.
        """

        raw_lines = document.text.splitlines()

        lines = []
        for raw_line in raw_lines:
            cleaned = self._clean_line(raw_line)

            if cleaned:
                lines.append(cleaned)

        requirements: List[Requirement] = []

        current_id: Optional[str] = None
        current_text: List[str] = []
        in_non_requirement_section = False

        for index, line in enumerate(lines):

            # Appendix/data-dictionary content is never a requirement.
            if re.match(
                r"^\s*(?:appendix|appendices|appendixes)\b",
                line,
                re.IGNORECASE,
            ):
                if current_text:
                    requirement = self._build_requirement(
                        current_id,
                        current_text,
                    )

                    if requirement:
                        requirements.append(requirement)

                current_id = None
                current_text = []
                in_non_requirement_section = True
                continue

            # Detect a non-requirement section heading embedded in
            # the same line as a requirement.
            embedded_non_requirement_section = (
                self._has_embedded_non_requirement_section(line)
            )

            # Detect numbered non-requirement sections such as:
            # 2. Assumptions
            # 2.1 Dependencies
            # 4. Appendixes
            if self.NON_REQUIREMENT_SECTION_PATTERN.match(line):
                if current_text:
                    requirement = self._build_requirement(
                        current_id,
                        current_text,
                    )

                    if requirement:
                        requirements.append(requirement)

                current_id = None
                current_text = []
                in_non_requirement_section = True
                continue

            # A new numbered section outside a non-requirement section
            # marks the return to normal document content.
            if self.NUMBERED_SECTION_PATTERN.match(line):
                if not in_non_requirement_section:
                    # Normal structural heading
                    if self._is_non_requirement_structure(line):
                        if current_text:
                            requirement = self._build_requirement(
                                current_id,
                                current_text,
                            )

                            if requirement:
                                requirements.append(requirement)

                        current_id = None
                        current_text = []
                        continue

                else:
                    # We have left the assumptions/dependencies/appendix section.
                    in_non_requirement_section = False

                    if self._is_structural_heading(line):
                        if current_text:
                            requirement = self._build_requirement(
                                current_id,
                                current_text,
                            )

                            if requirement:
                                requirements.append(requirement)

                        current_id = None
                        current_text = []
                        continue

            # Ignore everything inside a non-requirement section.
            if in_non_requirement_section:
                continue

            # Ignore other obvious structural/document metadata.
            if self._is_non_requirement_structure(line):
                if current_text:
                    requirement = self._build_requirement(
                        current_id,
                        current_text,
                    )

                    if requirement:
                        requirements.append(requirement)

                current_id = None
                current_text = []
                continue

            embedded_section_boundary = self._has_embedded_non_requirement_section(line)
            identifier_match = self.REQUIREMENT_ID_PATTERN.match(line)

            if identifier_match:
                requirement_id = identifier_match.group("id")
                requirement_text = identifier_match.group("text").strip()

                # Avoid treating document numbers as requirement IDs.
                if self._looks_like_document_identifier(
                    line,
                    requirement_id,
                ):
                    if current_text:
                        requirement = self._build_requirement(
                            current_id,
                            current_text,
                        )

                        if requirement:
                            requirements.append(requirement)

                    current_id = None
                    current_text = []
                    continue

                # Save previous requirement.
                if current_text:
                    requirement = self._build_requirement(
                        current_id,
                        current_text,
                    )

                    if requirement:
                        requirements.append(requirement)

                current_id = requirement_id
                current_text = [requirement_text]

                if embedded_section_boundary:
                    requirement = self._build_requirement(
                        current_id,
                        current_text,
                    )

                    if requirement:
                        requirements.append(requirement)

                    current_id = None
                    current_text = []
                    in_non_requirement_section = True

                    continue

                continue

            # If we have an identified requirement, determine whether
            # this is a new requirement or continuation.
            if current_id is not None:

                candidate = self.candidate_detector.detect(line)

                if (
                    candidate.is_candidate
                    and self._is_new_requirement_candidate(
                        line,
                        candidate.signals,
                    )
                ):
                    requirement = self._build_requirement(
                        current_id,
                        current_text,
                    )

                    if requirement:
                        requirements.append(requirement)

                    current_id = None
                    current_text = [line]
                    continue

                # Structural headings terminate the current requirement.
                if self._is_structural_heading(line):
                    requirement = self._build_requirement(
                        current_id,
                        current_text,
                    )

                    if requirement:
                        requirements.append(requirement)

                    current_id = None
                    current_text = []
                    continue

                current_text.append(line)
                continue

            # Handle unnumbered requirements.
            candidate = self.candidate_detector.detect(line)

            if candidate.is_candidate:
                requirements.append(
                    Requirement(
                        requirement_id=None,
                        text=line,
                    )
                )

        # Save final requirement.
        if current_text:
            requirement = self._build_requirement(
                current_id,
                current_text,
            )

            if requirement:
                requirements.append(requirement)

        return requirements

    def _is_new_requirement_candidate(
        self,
        text: str,
        signals,
    ) -> bool:
        """
        Determine whether a candidate line begins a new requirement.
        """

        if "explicit_id" in signals:
            return True

        if "user_story" in signals:
            return True

        stripped = text.strip()

        starts_like_requirement = re.match(
            r"^(?:"
            r"the\s+(?:system|application|platform|software|service|"
            r"interface|portal|website|backend|frontend|database)\b|"
            r"all\s+\w+\b|"
            r"users?\b|"
            r"customers?\b|"
            r"clients?\b|"
            r"administrators?\b|"
            r"operators?\b|"
            r"staff\b|"
            r"employees?\b|"
            r"response\s+time\b|"
            r"availability\b|"
            r"performance\b|"
            r"security\b"
            r")",
            stripped,
            re.IGNORECASE,
        )

        if starts_like_requirement:
            return True

        return False

    def _build_requirement(
        self,
        requirement_id: Optional[str],
        text_parts: List[str],
    ) -> Optional[Requirement]:
        """Build one complete Requirement from reconstructed text."""

        text = " ".join(text_parts)
        text = self._normalize_text(text)

        text = self._remove_embedded_structural_heading(text)

        if not text:
            return None

        # An explicit requirement ID is strong structural evidence.
        # The ID has already been separated from the requirement text,
        # so the candidate detector cannot see it here.
        if requirement_id is not None:
            return Requirement(
                requirement_id=requirement_id,
                text=text,
            )

        candidate = self.candidate_detector.detect(text)

        if not candidate.is_candidate:
            return None

        return Requirement(
            requirement_id=requirement_id,
            text=text,
        )

    @staticmethod
    def _clean_line(line: str) -> str:
        """Remove common extraction artifacts."""

        line = line.strip()

        line = re.sub(
            r"^[•▪◦‣]\s*",
            "",
            line,
        )

        line = re.sub(
            r"\s+",
            " ",
            line,
        )

        return line

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize reconstructed requirement text."""

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _is_non_requirement_structure(self, text: str) -> bool:
        """
        Detect standalone metadata, headings, table labels and other
        document structure that should not become requirements.
        """

        if self.PRIORITY_PATTERN.match(text):
            return True

        if self.TABLE_HEADER_PATTERN.match(text):
            return True

        if re.match(
            r"^\s*(?:"
            r"appendix|"
            r"appendices|"
            r"appendixes|"
            r"references?|"
            r"glossary|"
            r"data\s+dictionary|"
            r"table\s+of\s+contents"
            r")\b",
            text,
            re.IGNORECASE,
        ):
            return True

        if re.match(
            r"^\s*(?:module|chapter|section)\s+\d+",
            text,
            re.IGNORECASE,
        ):
            return True

        return self._is_structural_heading(text)

    def _looks_like_document_identifier(
        self,
        line: str,
        requirement_id: str,
    ) -> bool:
        """
        Avoid interpreting document numbers as requirement IDs.

        An ID-like token is treated as document metadata when the
        surrounding line explicitly identifies it as document/file/
        revision/version metadata.
        """

        if self.DOCUMENT_ID_CONTEXT_PATTERN.search(line):
            return True

        # A requirement ID followed by meaningful requirement text is
        # accepted. A standalone identifier is not.
        match = self.REQUIREMENT_ID_PATTERN.match(line)

        if not match:
            return False

        requirement_text = match.group("text").strip()

        if not requirement_text:
            return True

        return False

    def _is_structural_heading(self, text: str) -> bool:
        """Determine whether a line represents a structural heading."""

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

        if re.match(
            r"^(?:module|chapter|section)\s+\d+",
            text,
            re.IGNORECASE,
        ):
            return True

        return False


    def _remove_embedded_structural_heading(
        self,
        text: str,
    ) -> str:
        """
        Remove structural headings extracted on the same line as
        a requirement.
        """

        text = re.sub(
            r"\s+\d+(?:\.\d+)*\s+"
            r"(?:"
            r"System Features and Requirements|"
            r"Specific Requirements|"
            r"Appendixes|"
            r"Appendices|"
            r"Appendix"
            r")\b.*$",
            "",
            text,
            flags=re.IGNORECASE,
        )

        heading_pattern = re.compile(
            r"\s+(?:module|chapter|section)\s+"
            r"\d+(?::|\s+)[^:]*$",
            re.IGNORECASE,
        )

        text = heading_pattern.sub("", text)

        appendix_pattern = re.compile(
            r"\s+(Appendices|Appendix\s+[A-Z]\s*:)[^\n]*$",
            re.IGNORECASE,
        )

        text = appendix_pattern.sub("", text)

        return text.strip()


    def _has_embedded_non_requirement_section(self, text: str) -> bool:
        return bool(
            re.search(
                r"\s+\d+(?:\.\d+)*\s+"
                r"(?:"
                r"assumptions?|"
                r"dependencies?|"
                r"appendix|"
                r"appendixes|"
                r"appendices|"
                r"references?"
                r")\b.*$",
                text,
                re.IGNORECASE,
            )
        )