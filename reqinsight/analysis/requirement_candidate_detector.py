import re
from dataclasses import dataclass
from typing import List


@dataclass
class CandidateDetection:
    """
    Result of evaluating whether a text segment looks like
    a software requirement.
    """

    is_candidate: bool
    confidence: float
    signals: List[str]


class RequirementCandidateDetector:
    """
    Domain-agnostic detector for requirement-like text.

    The detector deliberately does NOT depend on domain-specific
    actors such as students, doctors, customers, educators, etc.
    """

    # Explicit requirement identifiers.
    #
    # Examples:
    # FR-01
    # NFR-09
    # FR-A-01
    # REQ-001
    # REQ-AUTH-002
    # AUTH-001
    # R001
    ID_PATTERN = re.compile(
        r"\b"
        r"[A-Za-z]{1,12}"
        r"(?:[-_][A-Za-z0-9]{1,20})*"
        r"\d{1,6}"
        r"\b"
    )

    MODAL_PATTERN = re.compile(
        r"\b("
        r"must|shall|should|may|"
        r"required to|"
        r"is required to|"
        r"are required to"
        r")\b",
        re.IGNORECASE,
    )

    CAPABILITY_PATTERNS = [
        re.compile(
            r"\bcan\s+(?:be\s+)?"
            r"(?:create|view|edit|delete|"
            r"search|download|upload|"
            r"add|remove|update|"
            r"manage|access|submit|"
            r"generate|send|receive|"
            r"configure|select|track|"
            r"filter|sort|export|import)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:is|are)\s+able\s+to\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\ballows?\s+(?:users?|customers?|"
            r"people|administrators?|actors?|"
            r"clients?|operators?)\s+to\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\benables?\s+(?:users?|customers?|"
            r"people|administrators?|actors?|"
            r"clients?|operators?)\s+to\b",
            re.IGNORECASE,
        ),
    ]

    USER_STORY_PATTERN = re.compile(
        r"^\s*"
        r"as\s+an?\s+.+?,"
        r"\s*i\s+(?:want|need|would like|should be able)"
        r"\b",
        re.IGNORECASE,
    )

    CONSTRAINT_PATTERNS = [
        re.compile(
            r"\b("
            r"response time|"
            r"availability|"
            r"uptime|"
            r"throughput|"
            r"concurrent users?|"
            r"maximum|minimum|"
            r"within\s+\d+|"
            r"less than\s+\d+|"
            r"greater than\s+\d+|"
            r"at least\s+\d+|"
            r"at most\s+\d+|"
            r"\d+\s*(?:ms|milliseconds|"
            r"seconds?|minutes?|hours?|%)"
            r")\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b("
            r"encrypted|"
            r"hashed|"
            r"authenticated|"
            r"authorized|"
            r"compliant with|"
            r"compatible with"
            r")\b",
            re.IGNORECASE,
        ),
    ]

    SYSTEM_ACTION_PATTERN = re.compile(
        r"\b("
        r"system|application|platform|software|"
        r"service|interface|portal|website|"
        r"mobile application|web application"
        r")\b"
        r".{0,80}\b("
        r"provide|provides|support|supports|"
        r"allow|allows|enable|enables|"
        r"offer|offers|perform|process|generate|"
        r"store|display|send|receive|"
        r"validate|calculate|manage|"
        r"maintain|record|track"
        r")\b",
        re.IGNORECASE,
    )

    ACTOR_ACTION_PATTERN = re.compile(
        r"\b("
        r"user|users|customer|customers|"
        r"administrator|administrators|"
        r"operator|operators|client|clients|"
        r"employee|employees|manager|managers|"
        r"staff|actor|actors"
        r")\b"
        r".{0,80}\b("
        r"can|may|must|shall|should|"
        r"able|access|create|view|"
        r"edit|delete|submit|download|"
        r"upload|search|select|manage|"
        r"receive|send|track"
        r")\b",
        re.IGNORECASE,
    )

    NEGATIVE_PATTERNS = [
        re.compile(
            r"^\s*(?:this|the)\s+document\s+"
            r"(?:describes|defines|specifies|"
            r"presents|provides)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\bproject\s+(?:team|will|schedule|"
            r"timeline|methodology)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\bwas\s+(?:developed|implemented|created)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"^\s*(?:table|figure|appendix|"
            r"references?|glossary|"
            r"data dictionary)\b",
            re.IGNORECASE,
        ),
    ]

    def detect(self, text: str) -> CandidateDetection:
        """
        Evaluate one text segment.

        Detection is based on several independent signals rather
        than a hard-coded list of domain-specific actors.
        """

        text = text.strip()

        if not text:
            return CandidateDetection(
                is_candidate=False,
                confidence=0.0,
                signals=[],
            )

        for pattern in self.NEGATIVE_PATTERNS:
            if pattern.search(text):
                return CandidateDetection(
                    is_candidate=False,
                    confidence=0.0,
                    signals=[],
                )

        signals = []
        score = 0.0

        if self.ID_PATTERN.search(text):
            signals.append("explicit_id")
            score += 0.45

        if self.MODAL_PATTERN.search(text):
            signals.append("modal")
            score += 0.35

        if self.USER_STORY_PATTERN.search(text):
            signals.append("user_story")
            score += 0.60

        if any(
            pattern.search(text)
            for pattern in self.CAPABILITY_PATTERNS
        ):
            signals.append("capability")
            score += 0.45

        if any(
            pattern.search(text)
            for pattern in self.CONSTRAINT_PATTERNS
        ):
            signals.append("constraint")
            score += 0.30

        if self.SYSTEM_ACTION_PATTERN.search(text):
            signals.append("system_action")
            score += 0.50

        if self.ACTOR_ACTION_PATTERN.search(text):
            signals.append("actor_action")
            score += 0.20

        # A requirement with an explicit ID is a strong candidate
        # even when the wording doesn't contain a modal verb.
        #
        # A user story is also strong evidence on its own.
        #
        # Other forms require multiple supporting signals.
        if "explicit_id" in signals:
            is_candidate = score >= 0.45

        elif "user_story" in signals:
            is_candidate = True

        elif "modal" in signals:
            is_candidate = score >= 0.35

        else:
            is_candidate = score >= 0.45

        confidence = min(score, 1.0)

        return CandidateDetection(
            is_candidate=is_candidate,
            confidence=confidence,
            signals=signals,
        )