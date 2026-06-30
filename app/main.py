# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, Form, Request
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
    recruiter_csv: Optional[UploadFile] = File(None),
    resume_pdf: Optional[UploadFile] = File(None),
    txt_file: Optional[UploadFile] = File(None),
    ats_json_file: Optional[UploadFile] = File(None),
    github_url: Optional[str] = Form(None),

    projection_config: Optional[str] = Form(None),
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
        github_url,
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
        # GitHub URL (string — no file needed)
        ####################################################

        if github_url:

            logger.info(
                f"[{request_id}] GitHub URL received: {github_url}"
            )

            pipeline_kwargs["github_url"] = github_url

        ####################################################
        # Execute Pipeline
        ####################################################

        logger.info(
            f"[{request_id}] Executing multi-source "
            f"transformation pipeline..."
        )

        response = pipeline.run(**pipeline_kwargs)

        ####################################################
        # Processing Time
        ####################################################

        elapsed = round(
            time.time() - start_time,
            3,
        )

        logger.info(
            f"[{request_id}] Pipeline completed "
            f"successfully in {elapsed}s"
        )

        ####################################################
        # Return Response
        ####################################################

        return {
            "success": True,
            "requestId": request_id,
            "processingTimeSeconds": elapsed,
            "data": response,
        }

    finally:

        ####################################################
        # Cleanup Temporary Files
        ####################################################

        try:

            for file_path in saved_files:
                if file_path.exists():
                    file_path.unlink()

            temp_dir.rmdir()

            logger.info(
                f"[{request_id}] Temporary files cleaned"
            )

        except Exception as cleanup_error:

            logger.warning(
                f"[{request_id}] Cleanup failed: {cleanup_error}"
            )


############################################################
# Individual Source Endpoints
############################################################


@app.post("/transform/github")
async def transform_github(
    request: Request,
    github_url: str = Form(...),
    projection_config: Optional[str] = Form(None),
):
    """Transform candidate data from a GitHub profile URL."""

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    
    config_dict = None
    if projection_config:
        try:
            config_dict = json.loads(projection_config)
        except json.JSONDecodeError:
            return JSONResponse(status_code=400, content={"success": False, "error": "Invalid JSON in projection_config"})

    logger.info(
        f"[{request_id}] GitHub-only transformation: {github_url}"
    )

    response = pipeline.run(github_url=github_url, projection_config=config_dict)

    elapsed = round(time.time() - start_time, 3)

    return {
        "success": True,
        "requestId": request_id,
        "processingTimeSeconds": elapsed,
        "data": response,
    }




@app.post("/transform/ats")
async def transform_ats(
    request: Request,
    ats_json_file: UploadFile = File(...),
    projection_config: Optional[str] = Form(None),
):
    """Transform candidate data from an ATS JSON file."""

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    
    config_dict = None
    if projection_config:
        try:
            config_dict = json.loads(projection_config)
        except json.JSONDecodeError:
            return JSONResponse(status_code=400, content={"success": False, "error": "Invalid JSON in projection_config"})

    temp_dir = Path(tempfile.mkdtemp())

    try:

        json_path = temp_dir / ats_json_file.filename

        with open(json_path, "wb") as buffer:
            shutil.copyfileobj(
                ats_json_file.file, buffer
            )

        ats_source = str(json_path)

        logger.info(
            f"[{request_id}] ATS-only transformation"
        )

        response = pipeline.run(ats_json=ats_source, projection_config=config_dict)

        elapsed = round(time.time() - start_time, 3)

        return {
            "success": True,
            "requestId": request_id,
            "processingTimeSeconds": elapsed,
            "data": response,
        }

    finally:

        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


@app.post("/transform/txt")
async def transform_txt(
    request: Request,
    txt_file: UploadFile = File(...),
    projection_config: Optional[str] = Form(None),
):
    """Transform candidate data from a plain text file."""

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    
    config_dict = None
    if projection_config:
        try:
            config_dict = json.loads(projection_config)
        except json.JSONDecodeError:
            return JSONResponse(status_code=400, content={"success": False, "error": "Invalid JSON in projection_config"})

    temp_dir = Path(tempfile.mkdtemp())

    try:

        txt_path = temp_dir / txt_file.filename

        with open(txt_path, "wb") as buffer:
            shutil.copyfileobj(
                txt_file.file, buffer
            )

        logger.info(
            f"[{request_id}] TXT-only transformation"
        )

        response = pipeline.run(txt_path=str(txt_path), projection_config=config_dict)

        elapsed = round(time.time() - start_time, 3)

        return {
            "success": True,
            "requestId": request_id,
            "processingTimeSeconds": elapsed,
            "data": response,
        }

    finally:

        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass