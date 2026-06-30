from app.logging.logger import logger


class SkillNormalizer:

    def normalize(self, skills):

        logger.info(
            f"Normalizing {len(skills)} skills..."
        )

        normalized = []

        seen = set()

        for skill in skills:

            skill = skill.strip().title()

            if skill not in seen:

                normalized.append(skill)

                seen.add(skill)

        logger.info(
            f"Skill normalization complete: "
            f"{len(normalized)} unique skills"
        )

        return normalized