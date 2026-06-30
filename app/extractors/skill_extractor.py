import re

from app.extractors.skills_db import SKILLS
from app.logging.logger import logger


class SkillExtractor:

    def extract(self, sections):

        logger.info("Extracting skills...")

        text = "\n".join(sections.get("skills", []))

        words = re.findall(
            r"[A-Za-z0-9.+#-]+",
            text
        )

        skills = []

        for word in words:

            if word.lower() in SKILLS:

                skills.append(word.title())

        result = sorted(set(skills))

        logger.info(
            f"Skills extracted: {len(result)} skills found"
        )

        return result