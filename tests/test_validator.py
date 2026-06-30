from app.validation.validator import CandidateValidator

from app.models.candidate import Candidate


def test_validation():

    candidate = Candidate(

        candidate_id="",

        full_name="",

        headline="",

        emails=[],

        phones=[],

        skills=[],

        education=[],

        experience=[],

        links={},

        years_experience=0,

        overall_confidence=0
    )

    result = CandidateValidator().validate(candidate)

    assert result.is_valid is False

    assert len(result.errors) > 0