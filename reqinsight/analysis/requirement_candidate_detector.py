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

    The detector relies on linguistic and structural evidence rather
    than specific application domains such as healthcare, banking,
    education, or e-commerce.
    """

    # Generic requirement identifiers.
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
        r"required\s+to|"
        r"is\s+required\s+to|"
        r"are\s+required\s+to"
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
            r"\ballows?\s+"
            r"(?:users?|customers?|people|"
            r"administrators?|actors?|"
            r"clients?|operators?|"
            r"staff|employees?)\s+to\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\benables?\s+"
            r"(?:users?|customers?|people|"
            r"administrators?|actors?|"
            r"clients?|operators?|"
            r"staff|employees?)\s+to\b",
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
            r"response\s+time|"
            r"availability|"
            r"uptime|"
            r"throughput|"
            r"concurrent\s+users?|"
            r"maximum|minimum|"
            r"within\s+\d+|"
            r"less\s+than\s+\d+|"
            r"greater\s+than\s+\d+|"
            r"at\s+least\s+\d+|"
            r"at\s+most\s+\d+|"
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
            r"compliant\s+with|"
            r"compatible\s+with"
            r")\b",
            re.IGNORECASE,
        ),
    ]

    SYSTEM_ACTION_PATTERN = re.compile(
        r"\b("
        r"system|application|platform|software|"
        r"service|interface|portal|website|"
        r"backend|frontend|database|"
        r"mobile\s+application|web\s+application"
        r")\b"
        r".{0,100}\b("
        r"provide|provides|support|supports|"
        r"allow|allows|enable|enables|"
        r"offer|offers|perform|process|generate|"
        r"store|display|send|receive|"
        r"validate|calculate|manage|"
        r"maintain|record|track|"
        r"encrypt|authenticate|authorize|"
        r"failover|interface|integrate"
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
        r".{0,100}\b("
        r"can|may|must|shall|should|"
        r"able|access|create|view|"
        r"edit|delete|submit|download|"
        r"upload|search|select|manage|"
        r"receive|send|track"
        r")\b",
        re.IGNORECASE,
    )

    # Definitions such as:
    # "Must: Indicates a mandatory requirement."
    DEFINITION_PATTERN = re.compile(
        r"^\s*(?:must|shall|should|may|can)\s*:"
        r"\s*(?:indicates?|means?|refers?\s+to)\b",
        re.IGNORECASE,
    )

    DOCUMENT_PURPOSE_PATTERN = re.compile(
        r"^\s*the\s+purpose\s+of\s+(?:this|the)\s+"
        r"(?:software\s+requirements?\s+specification|"
        r"SRS|requirements?\s+document)"
        r"\b",
        re.IGNORECASE,
    )

    DOCUMENT_REFERENCE_PATTERN = re.compile(
        r"^\s*.*\b(?:business\s+requirements?\s+document|"
        r"BRD|software\s+requirements?\s+specification|"
        r"SRS)\b"
        r".*\b(?:v\d+(?:\.\d+)*|version\s+\d+(?:\.\d+)*)\b",
        re.IGNORECASE,
    )

    STAKEHOLDER_NEED_PATTERN = re.compile(
        r"^\s*[A-Za-z][A-Za-z0-9 _-]*\s*:"
        r"\s*need(?:s)?\b",
        re.IGNORECASE,
    )

    DEPENDENCY_PATTERN = re.compile(
        r"\b(?:relies?\s+on|depends?\s+on|"
        r"dependent\s+on|requires?\s+an?\s+external)\b",
        re.IGNORECASE,
    )

    # Project/document instructions rather than system requirements.
    PROJECT_INSTRUCTION_PATTERN = re.compile(
        r"^\s*(?:the\s+)?"
        r"(?:development|project|engineering|implementation|"
        r"technical|documentation)\s+"
        r"(?:team|staff|group)\b",
        re.IGNORECASE,
    )

    # Metadata-style labels.
    METADATA_PATTERN = re.compile(
        r"^\s*(?:"
        r"document\s+(?:number|id|identifier|version|status)|"
        r"version|"
        r"prepared\s+by|"
        r"author|"
        r"date|"
        r"revision|"
        r"priority|"
        r"category|"
        r"requirement\s+id|"
        r"guideline\s+id"
        r")\s*:",
        re.IGNORECASE,
    )

    # Priority values extracted from Agile/backlog tables.
    PRIORITY_VALUE_PATTERN = re.compile(
        r"^\s*(?:"
        r"high|medium|low"
        r")\s*\("
        r"(?:must|should|could|won't|wont)"
        r"\)\s*$",
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
            r"data\s+dictionary)\b",
            re.IGNORECASE,
        ),
    ]

    def detect(self, text: str) -> CandidateDetection:
        """
        Evaluate one text segment.
        """

        text = text.strip()

        if not text:
            return CandidateDetection(
                is_candidate=False,
                confidence=0.0,
                signals=[],
            )

        negative_patterns = [
            *self.NEGATIVE_PATTERNS,
            self.DEFINITION_PATTERN,
            self.DOCUMENT_PURPOSE_PATTERN,
            self.DOCUMENT_REFERENCE_PATTERN,
            self.STAKEHOLDER_NEED_PATTERN,
            self.DEPENDENCY_PATTERN,
            self.PROJECT_INSTRUCTION_PATTERN,
            self.METADATA_PATTERN,
            self.PRIORITY_VALUE_PATTERN,
        ]

        for pattern in negative_patterns:
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

        # # A sentence with a modal is only a strong requirement candidate
        # # when it has an appropriate subject/action structure.
        # modal_has_subject = bool(
        #     re.search(
        #         r"^\s*(?:"
        #         r"the\s+\w+|"
        #         r"all\s+\w+|"
        #         r"users?\b|"
        #         r"customers?\b|"
        #         r"clients?\b|"
        #         r"administrators?\b|"
        #         r"operators?\b|"
        #         r"staff\b|"
        #         r"employees?\b|"
        #         r"the\s+system\b|"
        #         r"the\s+application\b|"
        #         r"the\s+platform\b|"
        #         r"the\s+service\b|"
        #         r"response\s+time\b|"
        #         r"response\s+times\b|"
        #         r"latency\b|"
        #         r"throughput\b|"
        #         r"availability\b|"
        #         r"uptime\b|"
        #         r"performance\b|"
        #         r"capacity\b|"
        #         r"load\b|"
        #         r"processing\s+time\b|"
        #         r"query\s+time\b|"
        #         r"startup\s+time\b"
        #         r")",
        #         text,
        #         re.IGNORECASE,
        #     )
        # )
        
        # A modal requirement may begin with virtually any meaningful
        # noun phrase. Do not maintain a domain-specific actor list.
        #
        # Examples:
        #   Doctors must create patient records.
        #   Nurses should update vital signs.
        #   Transaction processing must complete within 3 seconds.
        #   The system shall encrypt patient data.
        #
        # We deliberately allow generic noun phrases here because
        # ReqInsight must remain domain-agnostic.
        modal_has_subject = bool(
            re.search(
                r"^\s*"
                r"[A-Za-z][A-Za-z0-9_-]*"
                r"(?:\s+[A-Za-z][A-Za-z0-9_-]*){0,7}"
                r"\s+"
                r"(?:must|shall|should|may)\b",
                text,
                re.IGNORECASE,
            )
        )

        if "explicit_id" in signals:
            is_candidate = score >= 0.45

        elif "user_story" in signals:
            is_candidate = True

        elif "modal" in signals:
            is_candidate = (
                modal_has_subject
                and (
                    "system_action" in signals
                    or "actor_action" in signals
                    or "constraint" in signals
                    or "capability" in signals
                    or len(text.split()) >= 6
                )
            )

        else:
            is_candidate = score >= 0.45

        confidence = min(score, 1.0)

        return CandidateDetection(
            is_candidate=is_candidate,
            confidence=confidence,
            signals=signals,
        )