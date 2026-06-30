from app.projection.base_transformer import BaseTransformer

class CanonicalTransformer(BaseTransformer):
    def transform(self, value):
        if isinstance(value, list):
            return [self.transform(v) for v in value]
        if isinstance(value, str):
            return value.lower().strip()
        return value
