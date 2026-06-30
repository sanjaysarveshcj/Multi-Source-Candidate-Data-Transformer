from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str
    confidence: float = 1.0
    sources: List[str] = Field(default_factory=list)


class Experience(BaseModel):
    company: str
    title: str
    start: Optional[str] = None
    end: Optional[str] = None
    summary: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    field: Optional[str] = None
    end_year: Optional[int] = None


class Provenance(BaseModel):
    field: str
    source: str
    method: str


class Candidate(BaseModel):

    candidate_id: Optional[str] = None

    full_name: Optional[str] = None

    emails: List[str] = Field(default_factory=list)

    phones: List[str] = Field(default_factory=list)

    location: Dict = Field(default_factory=dict)

    links: Dict = Field(default_factory=dict)

    headline: Optional[str] = None

    years_experience: Optional[int] = None

    skills: List[Skill] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    provenance: List[Provenance] = Field(default_factory=list)

    overall_confidence: float = 0.0