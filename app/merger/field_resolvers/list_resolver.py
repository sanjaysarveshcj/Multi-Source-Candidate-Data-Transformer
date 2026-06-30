from app.logging.logger import logger


class ListResolver:

    def resolve(self, candidates, field):

        merged = []

        seen = set()

        sources = []

        for candidate in candidates:

            values = getattr(candidate, field)

            for value in values:

                if value not in seen:

                    seen.add(value)

                    merged.append(value)

                    sources.append(candidate.source)

        logger.info(
            f"List resolved '{field}': "
            f"{len(merged)} unique values from "
            f"{len(set(sources))} sources"
        )

        return merged, sources