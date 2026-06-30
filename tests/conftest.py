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

        skills=["Python", "Java"],

        education=[],

        experience=[],

        links=[],

        overall_confidence=0.95,

        years_experience=5
    )