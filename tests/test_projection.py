from app.projection.projector import CandidateProjector


def test_projection(sample_candidate):

    projector = CandidateProjector()

    result = projector.project(sample_candidate)

    assert result["basic"]["name"] == "John Doe"

    assert result["contact"]["primaryEmail"] == "john@gmail.com"

    assert result["profile"]["skillCount"] == 2