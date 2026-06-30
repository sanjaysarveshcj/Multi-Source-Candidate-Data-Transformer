from app.settings import SOURCE_PRIORITY
from app.logging.logger import logger


class NumericResolver:
    """
    Resolves a numeric field by picking the highest-priority
    non-None value.
    """

    def resolve(self, candidates, field):

        ordered = sorted(
            candidates,
            key=lambda c: SOURCE_PRIORITY.get(c.source, 999)
        )

        for candidate in ordered:

            value = getattr(candidate, field, None)

            if value is not None:

                logger.info(
                    f"Resolved '{field}' = {value} "
                    f"from source: {candidate.source}"
                )

                return value, [candidate.source]

        logger.info(
            f"No value found for field: '{field}'"
        )

        return None, []
