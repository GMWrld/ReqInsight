from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Document:
    """Represents an SRS document supplied to ReqInsight."""

    file_path: str
    file_name: str = field(init=False)
    file_type: str = field(init=False)
    text: str = ""
    requirements: List["Requirement"] = field(default_factory=list)

    def __post_init__(self) -> None:
        path = Path(self.file_path)
        self.file_name = path.name
        self.file_type = path.suffix.lower().lstrip(".")

    def add_requirement(self, requirement: "Requirement") -> None:
        self.requirements.append(requirement)

    @property
    def requirement_count(self) -> int:
        return len(self.requirements)
