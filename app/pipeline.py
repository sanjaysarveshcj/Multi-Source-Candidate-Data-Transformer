from app.sources.recruiter_csv import RecruiterCSVParser
from app.sources.resume_parser import ResumePDFParser
from app.extractors.resume_extractor import ResumeExtractor
from app.merger.merge_engine import MergeEngine
from app.validation.validator import CandidateValidator
from app.projection.projector import CandidateProjector


class CandidatePipeline:

    def __init__(self):

        self.csv_parser = RecruiterCSVParser()

        self.resume_parser = ResumePDFParser()

        self.resume_extractor = ResumeExtractor()

        self.merge_engine = MergeEngine()

        self.validator = CandidateValidator()   # <-- Add this

        self.projector = CandidateProjector()

    def run(self, csv_path, resume_path):

        ########################################
        # Parse recruiter CSV
        ########################################

        recruiter = self.csv_parser.parse(csv_path)

        ########################################
        # Parse resume PDF
        ########################################

        resume_text = self.resume_parser.parse(resume_path)

        ########################################
        # Extract resume information
        ########################################

        resume = self.resume_extractor.extract(resume_text)

        ########################################
        # Merge both candidates
        ########################################

        candidate = self.merge_engine.merge(
            [recruiter, resume]
        )

        ########################################
        # Validate merged candidate
        ########################################

        validation = self.validator.validate(candidate)

        ########################################
        # Return response
        ########################################

        projected_candidate = self.projector.project(candidate)

        return {
            "candidate": projected_candidate,
            "validation": validation.model_dump()
        }