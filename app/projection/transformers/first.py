from app.projection.base_transformer import BaseTransformer


class FirstTransformer(BaseTransformer):

    def transform(self, value):

        if isinstance(value, list):

            return value[0] if value else None

        return value