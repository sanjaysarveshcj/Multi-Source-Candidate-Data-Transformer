# pyrefly: ignore [missing-import]
import pytest

from app.models.candidate import Candidate


@pytest.fixture
def sample_candidate():

    return Candidate(

        candidate_id="123",

        full_name="John Doe",

        headline="Software Engineer",

        emails=["john@gmail.com"],

        phones=["9876543210"],

        skills=[
            {"name": "Python", "confidence": 0.85, "sources": ["Resume"]},
            {"name": "Java", "confidence": 0.85, "sources": ["Resume"]},
        ],

        education=[],

        experience=[],

        links={},

        overall_confidence=0.95,

        years_experience=5
    )