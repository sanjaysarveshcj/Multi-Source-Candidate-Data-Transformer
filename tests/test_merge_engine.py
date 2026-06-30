from app.merger.merge_engine import MergeEngine
from app.models.raw_candidate import RawCandidate


def test_merge():

    recruiter = RawCandidate(
        source="Recruiter CSV",
        full_name="John Doe",
        headline="Backend Engineer",
        emails=["a@gmail.com"],
        phones=[],
        skills=["Python"],
        education=[],
        experience=[],
        links=[]
    )

    resume = RawCandidate(
        source="Resume",
        full_name=None,
        headline=None,
        emails=["b@gmail.com"],
        phones=["9999999999"],
        skills=["Docker"],
        education=[],
        experience=[],
        links=[]
    )

    merged = MergeEngine().merge([recruiter, resume])

    assert merged.full_name == "John Doe"
    assert "Python" in merged.skills
    assert "Docker" in merged.skills
    assert "9999999999" in merged.phones