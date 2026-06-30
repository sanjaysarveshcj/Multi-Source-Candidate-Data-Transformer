import json
from app.pipeline import CandidatePipeline

def test():
    pipeline = CandidatePipeline()
    config = {
        "fields": [
            { "path": "full_name", "type": "string", "required": True },
            { "path": "primary_email", "from": "emails[0]", "type": "string", "required": True },
            { "path": "phone", "from": "phones[0]", "type": "string", "normalize": "E164" },
            { "path": "skills", "from": "skills[].name", "type": "string[]", "normalize": "canonical" }
        ],
        "include_confidence": True,
        "on_missing": "null"
    }

    print("Config used:", json.dumps(config, indent=2))
    
    try:
        res = pipeline.run(github_url="https://github.com/torvalds", projection_config=config)
        print("\nProjected output:", json.dumps(res["candidate"], indent=2))
        print("\nDynamic validation:", json.dumps(res["dynamic_validation"], indent=2))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test()
