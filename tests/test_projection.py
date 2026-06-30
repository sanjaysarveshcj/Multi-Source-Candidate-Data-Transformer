from app.projection.projector import CandidateProjector


def test_projection(sample_candidate):

    projector = CandidateProjector()

    result = projector.project(sample_candidate)

    assert result["full_name"] == "John Doe"

    assert result["emails"] == ["john@gmail.com"]

    assert len(result["skills"]) == 2