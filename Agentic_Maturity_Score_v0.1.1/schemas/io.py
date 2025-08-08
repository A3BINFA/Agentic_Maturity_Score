from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ResponseItem(BaseModel):
    ID: str | None = None
    Domain: str
    Question: str
    Weight: int = 3
    Answer: str
    Comments: str | None = None
    Evidence: str | None = None

class AssessmentInput(BaseModel):
    responses: List[ResponseItem]

class DomainScore(BaseModel):
    weighted_score: float
    level: int

class Scores(BaseModel):
    domains: Dict[str, DomainScore]
    overall: DomainScore

class RoadmapItem(BaseModel):
    id: str | None = None
    domain: str
    question: str
    current_score: int
    target_score: int
    gap: int
    recommended_action: str
    risk: str
    impact: str
    effort: str

class AssessmentResult(BaseModel):
    scores: Scores
    roadmap: List[RoadmapItem]

def get_schemas() -> Dict[str, Any]:
    return {
        "AssessmentInput": AssessmentInput.model_json_schema(),
        "AssessmentResult": AssessmentResult.model_json_schema()
    }
