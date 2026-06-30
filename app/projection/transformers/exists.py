from app.projection.base_transformer import BaseTransformer


class ExistsTransformer(BaseTransformer):

    def transform(self, value):

        if value is None:
            return False

        if isinstance(value, list):

            return len(value) > 0

        return bool(value)