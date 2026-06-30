from app.settings import SOURCE_PRIORITY
from app.logging.logger import logger


class ObjectListResolver:

    def resolve(self, candidates, field):

        merged = []
        sources = []

        ordered = sorted(
            candidates,
            key=lambda c: SOURCE_PRIORITY.get(c.source, 999)
        )

        for candidate in ordered:

            values = getattr(candidate, field)

            for obj in values:

                title = str(obj.get("title", obj.get("degree", ""))).lower().strip()
                company = str(obj.get("company", obj.get("institution", ""))).lower().strip()
                
                is_duplicate = False
                
                for existing in merged:
                    e_title = str(existing.get("title", existing.get("degree", ""))).lower().strip()
                    e_company = str(existing.get("company", existing.get("institution", ""))).lower().strip()
                    
                    if company and company == e_company:
                        if not title or not e_title or title == e_title:
                            is_duplicate = True
                            break

                if not is_duplicate:

                    merged.append(obj)

                    sources.append(candidate.source)

        logger.info(
            f"Object list resolved '{field}': "
            f"{len(merged)} unique objects from "
            f"{len(set(sources))} sources"
        )

        return merged, sources