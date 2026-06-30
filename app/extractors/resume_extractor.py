from app.models.raw_candidate import RawCandidate

from app.extractors.section_parser import SectionParser
from app.extractors.name_extractor import NameExtractor
from app.extractors.contact_extractor import ContactExtractor
from app.extractors.skill_extractor import SkillExtractor
from app.extractors.education_extractor import EducationExtractor
from app.extractors.experience_extractor import ExperienceExtractor
from app.logging.logger import logger
from app.exceptions.base_exception import CandidateTransformerException


class ResumeExtractor:

    def __init__(self):

        self.section_parser = SectionParser()

        self.name_extractor = NameExtractor()

        self.contact_extractor = ContactExtractor()

        self.skill_extractor = SkillExtractor()

        self.education_extractor = EducationExtractor()

        self.experience_extractor = ExperienceExtractor()

    def extract(self, text: str) -> RawCandidate:

        logger.info("Starting resume extraction...")

        try:

            sections = self.section_parser.split_sections(text)

            logger.info(
                f"Sections identified: {list(sections.keys())}"
            )

            contacts = self.contact_extractor.extract(text)

            logger.info(
                f"Contacts extracted: {len(contacts['emails'])} emails, "
                f"{len(contacts['phones'])} phones"
            )

            full_name = self.name_extractor.extract(
                "\n".join(sections["header"])
            )

            logger.info(
                f"Name extracted: {full_name}"
            )

            skills = self.skill_extractor.extract(sections)

            logger.info(
                f"Skills extracted: {len(skills)} skills"
            )

            education = self.education_extractor.extract(sections)

            logger.info(
                f"Education extracted: {len(education)} entries"
            )

            experience = self.experience_extractor.extract(sections)

            logger.info(
                f"Experience extracted: {len(experience)} entries"
            )

            logger.info("Resume extraction completed successfully")

            # Classify links into structured dict
            raw_links = contacts["links"]
            linkedin_links = contacts.get("linkedin", [])
            github_links = contacts.get("github", [])

            linkedin = linkedin_links[0] if linkedin_links else None
            github = github_links[0] if github_links else None

            # Remove linkedin/github from raw_links
            other = [
                link for link in raw_links
                if "linkedin.com" not in link.lower()
                and "github.com" not in link.lower()
            ]

            links = {
                "linkedin": linkedin,
                "github": github,
                "portfolio": None,
                "other": other,
            }

            return RawCandidate(

                source="Resume",

                full_name=full_name,

                emails=contacts["emails"],

                phones=contacts["phones"],

                links=links,

                skills=skills,

                education=education,

                experience=experience,
            )

        except CandidateTransformerException:
            raise

        except Exception as e:

            logger.error(
                f"Failed to extract resume data: {e}"
            )

            raise CandidateTransformerException(
                message=f"Failed to extract resume data: {e}",
                status_code=500,
                error_code="RESUME_EXTRACTION_ERROR",
            )