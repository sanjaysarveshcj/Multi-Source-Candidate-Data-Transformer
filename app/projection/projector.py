from pathlib import Path

import yaml

from app.projection.registry import TransformerRegistry


class CandidateProjector:

    def __init__(self):

        config_path = (
            Path(__file__).parent
            / "config"
            / "projection.yaml"
        )

        with open(config_path) as f:

            self.config = yaml.safe_load(f)

        self.registry = TransformerRegistry()

    ##############################################

    def _set_nested(self, output, path, value):

        keys = path.split(".")

        current = output

        for key in keys[:-1]:

            if key not in current:

                current[key] = {}

            current = current[key]

        current[keys[-1]] = value

    ##############################################

    def project(self, candidate):

        output = {}

        for output_field, config in self.config["fields"].items():

            source = config["source"]

            transform = config.get("transform")

            value = getattr(candidate, source, None)

            value = self.registry.transform(
                transform,
                value
            )

            self._set_nested(
                output,
                output_field,
                value
            )

        return output