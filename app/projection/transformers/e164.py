import re
from app.projection.base_transformer import BaseTransformer

class E164Transformer(BaseTransformer):
    def transform(self, value):
        if isinstance(value, list):
            return [self.transform(v) for v in value]
        if isinstance(value, str):
            digits = re.sub(r'[^\d]', '', value)
            if not digits:
                return value
            return '+' + digits
        return value
