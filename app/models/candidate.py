from typing import List, Optional, Dict
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field

from app.models.metadata import Provenance


class Candidate(BaseModel):
    candidate_id: Optional[str] = None

    full_name: Optional[str] = None

    emails: List[str] = Field(default_factory=list)

    phones: List[str] = Field(default_factory=list)

    headline: Optional[str] = None

    location: Dict = Field(default_factory=dict)

    years_experience: Optional[float] = None

    skills: List[dict] = Field(default_factory=list)

    experience: List[dict] = Field(default_factory=list)

    education: List[dict] = Field(default_factory=list)

    links: Dict = Field(default_factory=dict)

    provenance: List[Provenance] = Field(default_factory=list)

    overall_confidence: float = 0.0