from app.sources.recruiter_csv import RecruiterCSVParser
from app.sources.resume_parser import ResumePDFParser
from app.sources.github_parser import GitHubURLParser
from app.sources.linkedin_parser import LinkedInURLParser
from app.sources.ats_json_parser import ATSJsonParser
from app.sources.txt_parser import TxtFileParser

from app.extractors.resume_extractor import ResumeExtractor
from app.merger.merge_engine import MergeEngine
from app.validation.validator import CandidateValidator
from app.validation.dynamic_validator import DynamicSchemaValidator
from app.projection.projector import CandidateProjector
from app.logging.logger import logger


class CandidatePipeline:

    def __init__(self):

        self.csv_parser = RecruiterCSVParser()

        self.resume_parser = ResumePDFParser()

        self.resume_extractor = ResumeExtractor()

        self.github_parser = GitHubURLParser()

        self.linkedin_parser = LinkedInURLParser()

        self.ats_json_parser = ATSJsonParser()

        self.txt_parser = TxtFileParser()

        self.merge_engine = MergeEngine()

        self.validator = CandidateValidator()

        self.projector = CandidateProjector()

    def run(
        self,
        csv_path=None,
        resume_path=None,
        github_url=None,
        linkedin_url=None,
        ats_json=None,
        txt_path=None,
        projection_config=None,
    ):

        candidates = []

        sources_used = []

        ########################################
        # Parse recruiter CSV
        ########################################

        if csv_path:

            logger.info("Parsing Recruiter CSV...")

            recruiter = self.csv_parser.parse(csv_path)

            candidates.append(recruiter)

            sources_used.append("Recruiter CSV")

        ########################################
        # Parse resume PDF
        ########################################

        if resume_path:

            logger.info("Parsing Resume PDF...")

            resume_text = self.resume_parser.parse(
                resume_path
            )

            resume = self.resume_extractor.extract(
                resume_text
            )

            candidates.append(resume)

            sources_used.append("Resume")

        ########################################
        # Parse GitHub URL
        ########################################

        if github_url:

            logger.info("Parsing GitHub URL...")

            github = self.github_parser.parse(github_url)

            candidates.append(github)

            sources_used.append("GitHub")

        ########################################
        # Parse LinkedIn URL
        ########################################

        if linkedin_url:

            logger.info("Parsing LinkedIn URL...")

            linkedin = self.linkedin_parser.parse(
                linkedin_url
            )

            candidates.append(linkedin)

            sources_used.append("LinkedIn")

        ########################################
        # Parse ATS JSON blob
        ########################################

        if ats_json:

            logger.info("Parsing ATS JSON...")

            ats = self.ats_json_parser.parse(ats_json)

            candidates.append(ats)

            sources_used.append("ATS JSON")

        ########################################
        # Parse TXT file
        ########################################

        if txt_path:

            logger.info("Parsing TXT file...")

            txt = self.txt_parser.parse(txt_path)

            candidates.append(txt)

            sources_used.append("Text File")

        ########################################
        # Validate we have at least one source
        ########################################

        if not candidates:
            raise ValueError(
                "At least one data source must be "
                "provided for transformation."
            )

        ########################################
        # Merge all candidates
        ########################################

        candidate = self.merge_engine.merge(candidates)

        ########################################
        # Validate merged candidate
        ########################################

        validation = self.validator.validate(candidate)

        ########################################
        # Return response
        ########################################

        projected_candidate = self.projector.project(
            candidate,
            config=projection_config
        )
        
        dynamic_validation_result = None
        if projection_config:
            dynamic_validation_result = DynamicSchemaValidator.validate(
                projected_candidate,
                projection_config
            )

        return {
            "candidate": projected_candidate,
            "sources_used": sources_used,
            "validation": validation.model_dump(),
            "dynamic_validation": dynamic_validation_result
        }