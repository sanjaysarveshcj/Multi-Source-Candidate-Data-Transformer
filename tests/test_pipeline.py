from unittest.mock import MagicMock

from app.pipeline import CandidatePipeline


def test_pipeline():

    pipeline = CandidatePipeline()

    pipeline.csv_parser.parse = MagicMock()

    pipeline.resume_parser.parse = MagicMock()

    pipeline.resume_extractor.extract = MagicMock()

    pipeline.merge_engine.merge = MagicMock()

    pipeline.validator.validate = MagicMock()

    pipeline.projector.project = MagicMock()

    pipeline.run("a.csv", "resume.pdf")

    pipeline.csv_parser.parse.assert_called_once()

    pipeline.resume_parser.parse.assert_called_once()

    pipeline.resume_extractor.extract.assert_called_once()

    pipeline.merge_engine.merge.assert_called_once()

    pipeline.validator.validate.assert_called_once()

    pipeline.projector.project.assert_called_once()