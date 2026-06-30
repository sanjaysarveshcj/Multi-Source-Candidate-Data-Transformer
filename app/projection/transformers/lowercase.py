from app.projection.base_transformer import BaseTransformer


class LowercaseTransformer(BaseTransformer):

    def transform(self, value):

        if isinstance(value, str):

            return value.lower()

        return value