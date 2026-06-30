from app.logging.logger import logger


class LocationNormalizer:
    """
    Ensures location dict has the canonical keys:
    { city, region, country }

    Country should ideally be ISO-3166 alpha-2.
    """

    def normalize(self, location):

        if not isinstance(location, dict):
            return {"city": None, "region": None, "country": None}

        logger.info(
            f"Normalizing location: {location}"
        )

        normalized = {
            "city": location.get("city"),
            "region": location.get("region"),
            "country": location.get("country"),
        }

        # Ensure country is uppercase (ISO-3166 alpha-2)
        if normalized["country"] and isinstance(normalized["country"], str):
            code = normalized["country"].strip().upper()
            if len(code) == 2:
                normalized["country"] = code

        logger.info(
            f"Location normalization complete: {normalized}"
        )

        return normalized
