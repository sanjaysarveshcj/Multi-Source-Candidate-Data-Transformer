from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.metadata import Provenance


class Candidate(BaseModel):
    candidate_id: Optional[str] = None

    full_name: Optional[str] = None

    emails: List[str] = Field(default_factory=list)

    phones: List[str] = Field(default_factory=list)

    headline: Optional[str] = None

    location: Optional[str] = None

    skills: List[str] = Field(default_factory=list)

    experience: List[dict] = Field(default_factory=list)

    education: List[dict] = Field(default_factory=list)

    links: List[str] = Field(default_factory=list)

    provenance: List[Provenance] = Field(default_factory=list)

    overall_confidence: float = 0.0