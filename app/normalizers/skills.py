class SkillNormalizer:

    def normalize(self, skills):

        normalized = []

        seen = set()

        for skill in skills:

            skill = skill.strip().title()

            if skill not in seen:

                normalized.append(skill)

                seen.add(skill)

        return normalized