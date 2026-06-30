from typing import List, Optional, Dict
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str = Field(description="canonical skill names")
    confidence: float = 1.0
    sources: List[str] = Field(default_factory=list)


class Experience(BaseModel):
    company: str
    title: str
    start: Optional[str] = Field(None, description="dates as YYYY-MM")
    end: Optional[str] = Field(None, description="dates as YYYY-MM")
    summary: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    field: Optional[str] = None
    end_year: Optional[int] = None


class Location(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = Field(None, description="ISO-3166 alpha-2")


class Links(BaseModel):
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    other: List[str] = Field(default_factory=list)


class Provenance(BaseModel):
    field: str
    source: str
    method: str = Field(description="where each value came from")


class Candidate(BaseModel):

    candidate_id: str

    full_name: str

    emails: List[str] = Field(default_factory=list)

    phones: List[str] = Field(default_factory=list, description="E.164 format")

    location: Location = Field(default_factory=Location)

    links: Links = Field(default_factory=Links)

    headline: Optional[str] = None

    years_experience: Optional[float] = None

    skills: List[Skill] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    provenance: List[Provenance] = Field(default_factory=list)

    overall_confidence: float = 0.0