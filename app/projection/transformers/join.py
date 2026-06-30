from app.projection.base_transformer import BaseTransformer


class JoinTransformer(BaseTransformer):

    def transform(self, value):

        if isinstance(value, list):

            return ", ".join(str(v) for v in value)

        return value