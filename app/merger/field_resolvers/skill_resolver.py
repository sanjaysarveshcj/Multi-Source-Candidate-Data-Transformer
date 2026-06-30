from app.logging.logger import logger

class SkillResolver:

    def resolve(self, candidates, field):

        skill_map = {}
        all_sources = set()

        for candidate in candidates:

            values = getattr(candidate, field)
            source = candidate.source

            for skill in values:

                normalized_name = skill.strip().title()

                if normalized_name not in skill_map:
                    skill_map[normalized_name] = {
                        "name": normalized_name,
                        "confidence": 1.0,
                        "sources": []
                    }

                if source not in skill_map[normalized_name]["sources"]:
                    skill_map[normalized_name]["sources"].append(source)
                
                all_sources.add(source)

        merged = list(skill_map.values())

        logger.info(
            f"Skill list resolved '{field}': "
            f"{len(merged)} unique skills from "
            f"{len(all_sources)} sources"
        )

        return merged, list(all_sources)
