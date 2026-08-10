from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class Issue:
    """Represents a quality issue detected in a requirement."""

    rule_id: str
    issue_type: str
    message: str
    severity: Severity
    iso_characteristic: Optional[str] = None
    detected_text: Optional[str] = None
    recommendation: Optional[str] = None
