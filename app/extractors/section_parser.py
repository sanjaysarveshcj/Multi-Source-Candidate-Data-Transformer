import re

from app.logging.logger import logger


class SectionParser:

    HEADINGS = {
        "education": [
            "education",
            "academic",
            "qualification",
            "qualifications"
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment",
            "internship",
            "internships"
        ],
        "skills": [
            "skills",
            "technical skills",
            "technologies",
            "tech stack"
        ],
        "projects": [
            "projects",
            "project"
        ],
        "certifications": [
            "certifications",
            "certification",
            "licenses"
        ],
        "achievements": [
            "achievements",
            "awards",
            "accomplishments"
        ]
    }

    def split_sections(self, text: str):

        logger.info("Splitting text into sections...")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        sections = {
            "header": [],
            "education": [],
            "experience": [],
            "skills": [],
            "projects": [],
            "certifications": [],
            "achievements": []
        }

        current = "header"

        for line in lines:

            lower = line.lower()

            found = False

            for section, headings in self.HEADINGS.items():

                if any(
                    re.fullmatch(rf"{re.escape(h)}[:]?", lower)
                    for h in headings
                ):
                    current = section
                    found = True
                    logger.info(
                        f"Section detected: {section}"
                    )
                    break

            if found:
                continue

            sections[current].append(line)

        section_summary = {
            k: len(v) for k, v in sections.items() if v
        }

        logger.info(
            f"Section splitting complete: {section_summary}"
        )

        return sections