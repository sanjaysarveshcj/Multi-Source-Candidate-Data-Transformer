class SkillExtractor:

    def extract(self, section: str):

        if not section:
            return []

        skills = []

        for line in section.split("\n"):

            line = line.strip()

            if not line:
                continue

            line = line.replace("•", ",")

            line = line.replace("|", ",")

            line = line.replace("/", ",")

            parts = line.split(",")

            for part in parts:

                skill = part.strip()

                if skill:
                    skills.append(skill)

        return sorted(list(set(skills)))