import argparse
import json
import sys
from pathlib import Path

from app.pipeline import CandidatePipeline
from app.logging.logger import logger


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Source Candidate Transformer CLI"
    )
    
    parser.add_argument("--csv", type=str, help="Path to recruiter CSV file")
    parser.add_argument("--resume", type=str, help="Path to resume PDF file")
    parser.add_argument("--txt", type=str, help="Path to plain text file")
    parser.add_argument("--ats-json", type=str, help="Path to ATS JSON file")
    parser.add_argument("--github", type=str, help="GitHub profile URL")
    
    parser.add_argument(
        "--projection-config", 
        type=str, 
        help="Path to a JSON file containing the projection configuration"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        help="Path to save the output JSON (prints to stdout if not provided)"
    )
    
    args = parser.parse_args()
    
    has_source = any([
        args.csv,
        args.resume,
        args.txt,
        args.ats_json,
        args.github,
    ])
    
    if not has_source:
        print("Error: At least one data source must be provided.")
        parser.print_help()
        sys.exit(1)
        
    pipeline = CandidatePipeline()
    pipeline_kwargs = {}
    
    if args.csv:
        pipeline_kwargs["csv_path"] = args.csv
    if args.resume:
        pipeline_kwargs["resume_path"] = args.resume
    if args.txt:
        pipeline_kwargs["txt_path"] = args.txt
    if args.ats_json:
        pipeline_kwargs["ats_json"] = args.ats_json
    if args.github:
        pipeline_kwargs["github_url"] = args.github
        
    if args.projection_config:
        try:
            with open(args.projection_config, 'r') as f:
                pipeline_kwargs["projection_config"] = json.load(f)
        except Exception as e:
            print(f"Error reading projection config: {e}")
            sys.exit(1)
            
    logger.info("Executing transformation pipeline via CLI...")
    
    class PydanticEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, 'model_dump'):
                return obj.model_dump()
            return super().default(obj)
            
    try:
        result = pipeline.run(**pipeline_kwargs)
        
        output_json = json.dumps(result, indent=2, cls=PydanticEncoder)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_json)
            logger.info(f"Output saved to {args.output}")
        else:
            print(output_json)
            
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
