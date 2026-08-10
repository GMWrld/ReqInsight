from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from .document import Document
from .issue import Issue


@dataclass
class AnalysisReport:
    """Contains the results of analyzing one SRS document."""

    document: Document
    created_at: datetime = field(default_factory=datetime.now)
    issues: List[Issue] = field(default_factory=list)
    quality_score: float = 0.0

    @property
    def requirement_count(self) -> int:
        return self.document.requirement_count

    @property
    def issue_count(self) -> int:
        return len(self.issues)

    def add_issue(self, issue: Issue) -> None:
        self.issues.append(issue)
