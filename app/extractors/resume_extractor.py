from app.models.raw_candidate import RawCandidate

from app.extractors.section_parser import SectionParser
from app.extractors.name_extractor import NameExtractor
from app.extractors.contact_extractor import ContactExtractor
from app.extractors.skill_extractor import SkillExtractor
from app.extractors.education_extractor import EducationExtractor
from app.extractors.experience_extractor import ExperienceExtractor


class ResumeExtractor:

    def __init__(self):

        self.section_parser = SectionParser()

        self.name_extractor = NameExtractor()

        self.contact_extractor = ContactExtractor()

        self.skill_extractor = SkillExtractor()

        self.education_extractor = EducationExtractor()

        self.experience_extractor = ExperienceExtractor()

    def extract(self, text: str) -> RawCandidate:

        sections = self.section_parser.split_sections(text)

        contacts = self.contact_extractor.extract(text)

        return RawCandidate(

            source="Resume",

            full_name=self.name_extractor.extract(
                sections.get("header", "")
            ),

            emails=contacts["emails"],

            phones=contacts["phones"],

            links=contacts["links"],

            skills=self.skill_extractor.extract(
                sections.get("skills", "")
            ),

            education=self.education_extractor.extract(
                sections.get("education", "")
            ),

            experience=self.experience_extractor.extract(
                sections.get("experience", "")
            )
        )