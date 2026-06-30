from app.models.candidate import Candidate

from app.merger.field_registry import FIELD_CONFIG

from app.provenance.provenance_builder import ProvenanceBuilder

from app.confidence.confidence_engine import ConfidenceEngine

from app.utils.id_generator import CandidateIdGenerator

from app.logging.logger import logger


class MergeEngine:

    def __init__(self):

        self.provenance_builder = ProvenanceBuilder()

        self.confidence_engine = ConfidenceEngine()

        self.id_generator = CandidateIdGenerator()

    def merge(self, candidates):

        logger.info(
            f"Merging {len(candidates)} candidate sources: "
            f"{[c.source for c in candidates]}"
        )

        candidate = Candidate()

        provenance = []

        ############################################
        # Iterate over every registered field
        ############################################

        conflict_penalty = 0.0

        for field, config in FIELD_CONFIG.items():

            resolver = config["resolver"]

            normalizer = config["normalizer"]

            # Conflict Detection for scalar fields (String/Numeric)
            resolver_type = resolver.__class__.__name__
            if resolver_type in ("StringResolver", "NumericResolver"):
                unique_vals = set()
                for c in candidates:
                    val = getattr(c, field)
                    if val is not None and str(val).strip():
                        unique_vals.add(str(val).strip().lower())
                
                if len(unique_vals) > 1:
                    logger.warning(
                        f"Conflict detected in '{field}': {unique_vals}. Applying penalty."
                    )
                    conflict_penalty += 0.2

            value, sources = resolver.resolve(
                candidates,
                field
            )

            if normalizer is not None:

                value = normalizer.normalize(value)

            setattr(candidate, field, value)

            ##########################################
            # Provenance
            ##########################################

            for source in set(sources):

                provenance.append(

                    self.provenance_builder.build(

                        field,

                        source,

                        "merge"

                    )

                )

        ############################################
        # Overall Confidence
        ############################################

        scores = [

            self.confidence_engine.score(c.source)

            for c in candidates

        ]

        if scores:

            base_confidence = sum(scores) / len(scores)
            final_confidence = base_confidence - conflict_penalty
            
            # Clamp to [0.0, 1.0]
            candidate.overall_confidence = max(0.0, min(1.0, final_confidence))

        ############################################
        # Candidate ID
        ############################################

        candidate.candidate_id = (

            self.id_generator.generate(candidate)

        )

        ############################################
        # Provenance
        ############################################

        candidate.provenance = provenance

        logger.info(
            f"Merge complete: candidate_id={candidate.candidate_id}, "
            f"confidence={candidate.overall_confidence:.2f}"
        )

        return candidate