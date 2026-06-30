from app.projection.base_transformer import BaseTransformer


class LengthTransformer(BaseTransformer):

    def transform(self, value):

        if value is None:
            return 0

        return len(value)