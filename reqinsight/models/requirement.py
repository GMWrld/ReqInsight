from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Requirement:
    """Represents one requirement extracted from an SRS."""

    requirement_id: Optional[str]
    text: str
    section: Optional[str] = None
    issues: List["Issue"] = field(default_factory=list)

    def add_issue(self, issue: "Issue") -> None:
        self.issues.append(issue)

    @property
    def issue_count(self) -> int:
        return len(self.issues)
