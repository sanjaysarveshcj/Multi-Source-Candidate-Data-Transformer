from app.sources.recruiter_csv import RecruiterCSVParser
from app.sources.resume_parser import ResumePDFParser
from app.sources.github_parser import GitHubURLParser

from app.sources.ats_json_parser import ATSJsonParser
from app.sources.txt_parser import TxtFileParser

from app.extractors.resume_extractor import ResumeExtractor
from app.merger.merge_engine import MergeEngine
from app.merger.identity_resolver import IdentityResolver
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



        self.ats_json_parser = ATSJsonParser()

        self.txt_parser = TxtFileParser()

        self.identity_resolver = IdentityResolver()
        self.merge_engine = MergeEngine()

        self.validator = CandidateValidator()

        self.projector = CandidateProjector()

    def run(
        self,
        csv_path=None,
        resume_path=None,
        github_url=None,

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
            try:
                logger.info("Parsing Recruiter CSV...")
                recruiter = self.csv_parser.parse(csv_path)
                candidates.extend(recruiter)
                sources_used.append("Recruiter CSV")
            except Exception as e:
                logger.warning(f"Failed to parse Recruiter CSV: {e}")

        ########################################
        # Parse resume PDF
        ########################################

        if resume_path:
            try:
                logger.info("Parsing Resume PDF...")
                resume_chunks = self.resume_parser.parse(
                    resume_path
                )
                for chunk in resume_chunks:
                    resume = self.resume_extractor.extract(chunk)
                    candidates.extend(resume)
                sources_used.append("Resume")
            except Exception as e:
                logger.warning(f"Failed to parse Resume PDF: {e}")

        ########################################
        # Parse GitHub URL
        ########################################

        if github_url:
            try:
                logger.info("Parsing GitHub URL...")
                github = self.github_parser.parse(github_url)
                candidates.extend(github)
                sources_used.append("GitHub")
            except Exception as e:
                logger.warning(f"Failed to parse GitHub URL: {e}")



        ########################################
        # Parse ATS JSON blob
        ########################################

        if ats_json:
            try:
                logger.info("Parsing ATS JSON...")
                ats = self.ats_json_parser.parse(ats_json)
                candidates.extend(ats)
                sources_used.append("ATS JSON")
            except Exception as e:
                logger.warning(f"Failed to parse ATS JSON: {e}")

        ########################################
        # Parse TXT file
        ########################################

        if txt_path:
            try:
                logger.info("Parsing TXT file...")
                txt = self.txt_parser.parse(txt_path)
                candidates.extend(txt)
                sources_used.append("Text File")
            except Exception as e:
                logger.warning(f"Failed to parse TXT file: {e}")

        ########################################
        # Validate we have at least one source
        ########################################

        if not candidates:
            raise ValueError(
                "At least one data source must be "
                "provided for transformation."
            )

        ########################################
        # Resolve Identities & Merge
        ########################################

        grouped_candidates = self.identity_resolver.group(candidates)

        results = []

        for group in grouped_candidates:
            candidate = self.merge_engine.merge(group)
            
            validation = self.validator.validate(candidate)

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
            
            results.append({
                "candidate": projected_candidate,
                "validation": validation.model_dump(),
                "dynamic_validation": dynamic_validation_result,
                "sources_used": list(set([c.source for c in group]))
            })

        return {
            "data": results,
            "total_candidates": len(results),
            "sources_used": sources_used,
        }