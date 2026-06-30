from app.logging.logger import logger


class LinksNormalizer:
    """
    Ensures links dict has the canonical keys:
    { linkedin, github, portfolio, other[] }
    """

    def normalize(self, links):

        if not isinstance(links, dict):
            return {
                "linkedin": None,
                "github": None,
                "portfolio": None,
                "other": [],
            }

        logger.info(
            f"Normalizing links: {links}"
        )

        normalized = {
            "linkedin": links.get("linkedin"),
            "github": links.get("github"),
            "portfolio": links.get("portfolio"),
            "other": links.get("other", []),
        }

        # Ensure 'other' is always a list
        if not isinstance(normalized["other"], list):
            normalized["other"] = (
                [normalized["other"]]
                if normalized["other"]
                else []
            )

        logger.info(
            f"Links normalization complete: {normalized}"
        )

        return normalized
