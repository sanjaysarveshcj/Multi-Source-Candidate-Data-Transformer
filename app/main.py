# pyrefly: ignore [missing-import]
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, Form, Request, BackgroundTasks, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.responses import HTMLResponse
# pyrefly: ignore [missing-import]
from fastapi.templating import Jinja2Templates
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse
from typing import Optional
from pathlib import Path
import tempfile
import shutil
import uuid
import time
import json

from app.pipeline import CandidatePipeline
from app.logging.logger import logger

from app.handlers.exception_handlers import (
    candidate_exception_handler,
    generic_exception_handler,
)

from app.exceptions.base_exception import (
    CandidateTransformerException,
)

############################################################
# FastAPI App
############################################################

app = FastAPI(
    title="Multi-Source Candidate Transformer Service",
    description=(
        "Transforms candidate data from multiple sources "
        "(CSV, Resume PDF, GitHub URL, "
        "ATS JSON, TXT) into a unified Candidate Profile"
    ),
    version="2.0.0",
)

############################################################
# Register Exception Handlers
############################################################

app.add_exception_handler(
    CandidateTransformerException,
    candidate_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

############################################################
# Pipeline
############################################################

pipeline = CandidatePipeline()
templates = Jinja2Templates(directory="templates")

############################################################
# Job Store (In-Memory for Background Processing)
############################################################

jobs = {}

def process_background(job_id: str, pipeline_kwargs: dict, saved_files: list, temp_dir: Path):
    
    start_time = time.time()
    jobs[job_id] = {"status": "processing", "data": None, "error": None}
    
    try:
        logger.info(f"[{job_id}] Executing background pipeline...")
        response = pipeline.run(**pipeline_kwargs)
        
        elapsed = round(time.time() - start_time, 3)
        logger.info(f"[{job_id}] Pipeline completed successfully in {elapsed}s")
        
        jobs[job_id] = {
            "status": "completed", 
            "data": response, 
            "processingTimeSeconds": elapsed,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"[{job_id}] Background pipeline failed: {e}")
        jobs[job_id] = {"status": "failed", "data": None, "error": str(e)}
        
    finally:
        # Cleanup Temporary Files
        try:
            for file_path in saved_files:
                if file_path.exists():
                    file_path.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()
            logger.info(f"[{job_id}] Temporary files cleaned")
        except Exception as cleanup_error:
            logger.warning(f"[{job_id}] Cleanup failed: {cleanup_error}")

############################################################
# Job Status Endpoint
############################################################

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {
        "success": True,
        "job_id": job_id,
        "status": jobs[job_id]["status"],
        "data": jobs[job_id].get("data"),
        "error": jobs[job_id].get("error"),
        "processingTimeSeconds": jobs[job_id].get("processingTimeSeconds")
    }

############################################################
# Web UI Endpoint
############################################################

@app.get("/ui", response_class=HTMLResponse, tags=["UI"])
async def get_ui(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

############################################################
# Health Check
############################################################


@app.get("/")
def health():

    logger.info("Health check called")

    return {
        "status": "UP",
        "service": "Multi-Source Candidate Transformer",
        "version": "2.0.0",
        "supported_sources": [
            "Recruiter CSV",
            "Resume PDF",
            "GitHub URL",
            "ATS JSON",
            "Text File",
        ],
    }


############################################################
# Multi-Source Transform Endpoint
############################################################


@app.post("/transform")
async def transform(
    request: Request,
    background_tasks: BackgroundTasks,
    recruiter_csv: Optional[UploadFile] = File(None),
    resume_pdf: Optional[UploadFile] = File(None),
    txt_file: Optional[UploadFile] = File(None),
    ats_json_file: Optional[UploadFile] = File(None),
    github_urls: Optional[str] = Form(None),
    projection_config: Optional[str] = Form(""),
):

    ########################################################
    # Request ID
    ########################################################

    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.time()

    logger.info(
        f"[{request_id}] Incoming multi-source transformation request"
    )

    ########################################################
    # Validate at least one source
    ########################################################

    has_source = any([
        recruiter_csv,
        resume_pdf,
        txt_file,
        ats_json_file,
        github_urls,
    ])

    if not has_source:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "At least one data source is required.",
                "supported_sources": [
                    "recruiter_csv (file)",
                    "resume_pdf (file)",
                    "txt_file (file)",
                    "ats_json_file (file)",
                    "github_url (form field)",
                ],
            },
        )

    ########################################################
    # Temporary Directory
    ########################################################

    temp_dir = Path(tempfile.mkdtemp())

    saved_files = []

    try:
        config_dict = None
        if projection_config:
            try:
                config_dict = json.loads(projection_config)
            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "error": "Invalid JSON in projection_config"}
                )

        ####################################################
        # Pipeline kwargs
        ####################################################

        pipeline_kwargs = {}
        if config_dict:
            pipeline_kwargs["projection_config"] = config_dict

        ####################################################
        # Save Recruiter CSV
        ####################################################

        if recruiter_csv:

            logger.info(
                f"[{request_id}] Saving recruiter CSV..."
            )

            csv_path = temp_dir / recruiter_csv.filename

            with open(csv_path, "wb") as buffer:
                shutil.copyfileobj(
                    recruiter_csv.file, buffer
                )

            saved_files.append(csv_path)

            pipeline_kwargs["csv_path"] = str(csv_path)

        ####################################################
        # Save Resume PDF
        ####################################################

        if resume_pdf:

            logger.info(
                f"[{request_id}] Saving resume PDF..."
            )

            resume_path = temp_dir / resume_pdf.filename

            with open(resume_path, "wb") as buffer:
                shutil.copyfileobj(
                    resume_pdf.file, buffer
                )

            saved_files.append(resume_path)

            pipeline_kwargs["resume_path"] = str(
                resume_path
            )

        ####################################################
        # Save TXT File
        ####################################################

        if txt_file:

            logger.info(
                f"[{request_id}] Saving TXT file..."
            )

            txt_path = temp_dir / txt_file.filename

            with open(txt_path, "wb") as buffer:
                shutil.copyfileobj(
                    txt_file.file, buffer
                )

            saved_files.append(txt_path)

            pipeline_kwargs["txt_path"] = str(txt_path)

        ####################################################
        # Save ATS JSON File
        ####################################################

        if ats_json_file:

            logger.info(
                f"[{request_id}] Saving ATS JSON file..."
            )

            json_path = temp_dir / ats_json_file.filename

            with open(json_path, "wb") as buffer:
                shutil.copyfileobj(
                    ats_json_file.file, buffer
                )

            saved_files.append(json_path)

            pipeline_kwargs["ats_json"] = str(json_path)

        ####################################################
        # GitHub URLs (string — no file needed)
        ####################################################

        if github_urls:

            logger.info(
                f"[{request_id}] GitHub URLs received: {github_urls}"
            )

            github_urls_list = [url.strip() for url in github_urls.split(",") if url.strip()]
            pipeline_kwargs["github_urls"] = github_urls_list

        ####################################################
        # Execute Pipeline (Background)
        ####################################################

        jobs[request_id] = {"status": "pending", "data": None, "error": None}
        background_tasks.add_task(process_background, request_id, pipeline_kwargs, saved_files, temp_dir)

        return {
            "success": True,
            "job_id": request_id,
            "message": "Processing started in the background."
        }

    except Exception as e:
        
        # Cleanup Temporary Files if failed before background task
        try:
            for file_path in saved_files:
                if file_path.exists():
                    file_path.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()
        except Exception:
            pass
            
        raise e

