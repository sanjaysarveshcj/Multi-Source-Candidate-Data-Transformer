from app.settings import SOURCE_PRIORITY
from app.logging.logger import logger


class DictResolver:
    """
    Resolves a dict field by merging dicts from all sources.
    Higher-priority sources win for overlapping keys.
    """

    def resolve(self, candidates, field):

        ordered = sorted(
            candidates,
            key=lambda c: SOURCE_PRIORITY.get(c.source, 999)
        )

        merged = {}

        sources = []

        for candidate in ordered:

            value = getattr(candidate, field, {})

            if not isinstance(value, dict):
                continue

            for k, v in value.items():

                if v and k not in merged:

                    merged[k] = v

                    if candidate.source not in sources:
                        sources.append(candidate.source)

        logger.info(
            f"Dict resolved '{field}': "
            f"{len(merged)} keys from "
            f"{len(sources)} sources"
        )

        return merged, sources
