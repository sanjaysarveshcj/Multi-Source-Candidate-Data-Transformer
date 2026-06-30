class EducationExtractor:

    def extract(self, section: str):

        if not section:
            return []

        education = []

        for line in section.split("\n"):

            line = line.strip()

            if line:

                education.append(
                    {
                        "raw": line
                    }
                )

        return education