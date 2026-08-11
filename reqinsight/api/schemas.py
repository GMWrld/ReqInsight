from pydantic import BaseModel
from typing import List


class FindingResponse(BaseModel):
    rule: str
    severity: str
    message: str
    recommendation: str


class RequirementResponse(BaseModel):
    id: str
    text: str
    score: float
    classification: str
    findings: List[FindingResponse]


class DocumentResponse(BaseModel):
    file_name: str
    requirement_count: int


class SummaryResponse(BaseModel):
    score: float
    classification: str
    total_requirements: int
    excellent: int
    good: int
    needs_review: int
    poor: int


class AnalysisResponse(BaseModel):
    document: DocumentResponse
    summary: SummaryResponse
    requirements: List[RequirementResponse]