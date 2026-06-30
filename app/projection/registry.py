from app.projection.transformers.first import FirstTransformer
from app.projection.transformers.length import LengthTransformer
from app.projection.transformers.exists import ExistsTransformer
from app.projection.transformers.count import CountTransformer
from app.projection.transformers.join import JoinTransformer
from app.projection.transformers.uppercase import UppercaseTransformer
from app.projection.transformers.lowercase import LowercaseTransformer
from app.projection.transformers.skill_objects import SkillObjectTransformer
from app.projection.transformers.e164 import E164Transformer
from app.projection.transformers.canonical import CanonicalTransformer
from app.logging.logger import logger


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

            "to_skill_objects": SkillObjectTransformer(),

            "E164": E164Transformer(),

            "canonical": CanonicalTransformer(),

        }

    def transform(self, name, value):

        if name is None:

            return value

        transformer = self.registry.get(name)

        if transformer is None:

            logger.error(
                f"Unknown transformer requested: {name}"
            )

            raise ValueError(
                f"Unknown transformer: {name}"
            )

        logger.info(
            f"Applying transformer: {name}"
        )

        return transformer.transform(value)