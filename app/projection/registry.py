from app.projection.transformers.first import FirstTransformer
from app.projection.transformers.length import LengthTransformer
from app.projection.transformers.exists import ExistsTransformer
from app.projection.transformers.count import CountTransformer
from app.projection.transformers.join import JoinTransformer
from app.projection.transformers.uppercase import UppercaseTransformer
from app.projection.transformers.lowercase import LowercaseTransformer


class TransformerRegistry:

    def __init__(self):

        self.registry = {

            "first": FirstTransformer(),

            "length": LengthTransformer(),

            "exists": ExistsTransformer(),

            "count": CountTransformer(),

            "join": JoinTransformer(),

            "uppercase": UppercaseTransformer(),

            "lowercase": LowercaseTransformer(),

        }

    def transform(self, name, value):

        if name is None:

            return value

        transformer = self.registry.get(name)

        if transformer is None:

            raise ValueError(
                f"Unknown transformer: {name}"
            )

        return transformer.transform(value)