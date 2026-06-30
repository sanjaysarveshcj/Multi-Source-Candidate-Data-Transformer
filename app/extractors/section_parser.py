class SectionParser:

    SECTION_ALIASES = {
        "skills": "skills",
        "technical skills": "skills",
        "core competencies": "skills",

        "experience": "experience",
        "work experience": "experience",
        "professional experience": "experience",
        "employment history": "experience",

        "education": "education",
        "academic qualifications": "education",

        "projects": "projects",
        "certifications": "certifications",
        "summary": "summary",
        "profile": "summary",
    }

    def split_sections(self, text: str):

        sections = {"header": []}

        current = "header"

        for line in text.splitlines():

            clean = line.strip()

            if not clean:
                continue

            lower = clean.lower()

            if lower in self.SECTION_ALIASES:
                current = self.SECTION_ALIASES[lower]

                sections.setdefault(current, [])

            else:
                sections.setdefault(current, []).append(clean)

        return {
            key: "\n".join(value)
            for key, value in sections.items()
        }