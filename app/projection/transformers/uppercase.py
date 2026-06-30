from app.projection.base_transformer import BaseTransformer


class UppercaseTransformer(BaseTransformer):

    def transform(self, value):

        if isinstance(value, str):

            return value.upper()

        return value