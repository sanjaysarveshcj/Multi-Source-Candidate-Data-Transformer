from typing import List, Optional, Dict
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field


class RawCandidate(BaseModel):
    source: str

    full_name: Optional[str] = None

    emails: List[str] = Field(default_factory=list)

    phones: List[str] = Field(default_factory=list)

    headline: Optional[str] = None

    location: Dict = Field(default_factory=dict)

    years_experience: Optional[float] = None

    skills: List[str] = Field(default_factory=list)

    experience: List[dict] = Field(default_factory=list)

    education: List[dict] = Field(default_factory=list)

    links: Dict = Field(default_factory=dict)