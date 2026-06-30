class ExperienceExtractor:

    def extract(self, section: str):

        if not section:
            return []

        experience = []

        for line in section.split("\n"):

            line = line.strip()

            if line:

                experience.append(
                    {
                        "raw": line
                    }
                )

        return experience