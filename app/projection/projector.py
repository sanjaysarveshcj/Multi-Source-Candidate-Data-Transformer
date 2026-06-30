from pathlib import Path

from app.projection.registry import TransformerRegistry
from app.projection.path_extractor import PathExtractor
from app.exceptions.projection_exception import ProjectionException
from app.logging.logger import logger


class CandidateProjector:

    def __init__(self):
        self.registry = TransformerRegistry()
        self.default_config = {
            "fields": [
                { "path": "candidate_id", "type": "string" },
                { "path": "full_name", "type": "string" },
                { "path": "emails", "type": "string[]" },
                { "path": "phones", "type": "string[]" },
                { "path": "location", "type": "object" },
                { "path": "links", "type": "object" },
                { "path": "headline", "type": "string" },
                { "path": "years_experience", "type": "number" },
                { "path": "skills", "type": "object[]", "normalize": "to_skill_objects" },
                { "path": "experience", "type": "object[]" },
                { "path": "education", "type": "object[]" },
                { "path": "provenance", "type": "object[]" },
                { "path": "overall_confidence", "type": "number" },
            ],
            "on_missing": "null",
            "include_confidence": True
        }

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

    def project(self, candidate, config=None):

        logger.info("Starting candidate projection...")

        cfg = config if config else self.default_config
        output = {}

        on_missing = cfg.get("on_missing", "null")
        include_confidence = cfg.get("include_confidence", True)

        for field_cfg in cfg.get("fields", []):
            out_path = field_cfg.get("path")
            in_path = field_cfg.get("from", out_path)

            if not out_path:
                continue

            if not include_confidence and ("confidence" in out_path.lower() or out_path == "overall_confidence"):
                continue

            value = PathExtractor.extract(candidate, in_path)

            transform_name = field_cfg.get("normalize")
            if transform_name and value is not None:
                value = self.registry.transform(transform_name, value)

            is_empty = value is None or (isinstance(value, (list, dict, str)) and not value)
            if is_empty:
                if on_missing == "omit":
                    continue
                elif on_missing == "error" and field_cfg.get("required"):
                    raise ProjectionException(f"Missing required field: {out_path}")
                else:
                    value = None

            self._set_nested(output, out_path, value)

        logger.info(
            f"Projection complete: {len(output)} top-level fields"
        )

        return output