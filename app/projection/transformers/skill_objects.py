from app.projection.base_transformer import BaseTransformer


class SkillObjectTransformer(BaseTransformer):
    """
    Transforms a list of skill name strings into the
    canonical skill object format:
    [{ name, confidence, sources[] }]
    """

    def transform(self, value):
        
        # Skills are now natively merged into objects by SkillResolver
        # Return as is if it's already a list of dicts.
        if isinstance(value, list) and all(isinstance(v, dict) for v in value):
            return value

        # Fallback (shouldn't be reached if SkillResolver is used)
        if not isinstance(value, list):
            return []

        return [
            {
                "name": str(skill),
                "confidence": 0.5,
                "sources": [],
            }
            for skill in value
        ]
