from app.projection.base_transformer import BaseTransformer


class CountTransformer(BaseTransformer):

    def transform(self, value):

        if isinstance(value, list):

            return len(value)

        return 0