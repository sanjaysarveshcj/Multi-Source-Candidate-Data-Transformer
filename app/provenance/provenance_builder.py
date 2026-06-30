from app.models.metadata import Provenance
from app.logging.logger import logger


class ProvenanceBuilder:

    def build(self, field, source, method="merge"):

        logger.info(
            f"Building provenance: field={field}, "
            f"source={source}, method={method}"
        )

        return Provenance(
            field=field,
            source=source,
            method=method,
        )