import json
from app.models.raw_candidate import RawCandidate
from app.merger.merge_engine import MergeEngine
from app.projection.projector import CandidateProjector
from app.validation.dynamic_validator import DynamicSchemaValidator

def run_edge_case_tests():
    print("--- Edge Case Test: Conflict Resolution & Missing Data Omission ---\n")
    
    # 1. Setup mock sources
    # GitHub (lower trust, unstructured location, extra skills)
    github_candidate = RawCandidate(
        source="GitHub",
        full_name="Linus Torvalds",
        location={"raw": "Portland, OR"},
        skills=["C", "C++", "Linux Kernel"]
    )
    
    # ATS (higher trust, structured location, no skills but has phone)
    ats_candidate = RawCandidate(
        source="ATS",
        full_name="Linus B. Torvalds",  # Should win due to higher ATS trust
        location={"city": "Portland", "region": "Oregon", "country": "US"},
        phones=["(555) 019-9123"],
        skills=[] 
    )
    
    # 2. Merge
    print("[1] Merging ATS and GitHub sources...")
    engine = MergeEngine()
    merged = engine.merge([github_candidate, ats_candidate])
    print(f" -> Merged Canonical Name: {merged.full_name} (Resolved from ATS)")
    print(f" -> Merged Skills: {merged.skills} (Unioned from GitHub)")
    
    # 3. Project with edge case config
    # We use "on_missing": "omit" to verify it drops keys completely rather than returning null.
    # We also attempt to map a deep path (skills[].name) over a list of strings, which yields empty.
    config = {
        "fields": [
            { "path": "name", "from": "full_name", "type": "string" },
            { "path": "phone_number", "from": "phones[0]", "type": "string", "normalize": "E164" },
            { "path": "primary_email", "from": "emails[0]", "type": "string" }, # Doesn't exist
            { "path": "extracted_skills", "from": "skills[].name", "type": "string[]" } # Invalid deep path for strings
        ],
        "include_confidence": False,
        "on_missing": "omit"
    }
    
    print("\n[2] Applying Projection Config (on_missing: omit):")
    
    projector = CandidateProjector()
    projected = projector.project(merged, config)
    
    print("\n[3] Projected Output (Gold Profile):")
    print(json.dumps(projected, indent=2))
    
    # Notice that `primary_email` and `extracted_skills` are completely omitted from the dictionary!
    
    # 4. Validate
    validation = DynamicSchemaValidator.validate(projected, config)
    print("\n[4] Dynamic Validation:")
    print(json.dumps(validation, indent=2))

if __name__ == "__main__":
    run_edge_case_tests()
