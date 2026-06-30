from fastapi import FastAPI, UploadFile, File, Request
from pathlib import Path
import tempfile
import shutil
import uuid
import time

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
    title="Candidate Transformer Service",
    description="Transforms recruiter CSV + Resume PDF into a unified Candidate Profile",
    version="1.0.0",
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
        "service": "Candidate Transformer",
        "version": "1.0.0",
    }


############################################################
# Transform Endpoint
############################################################


@app.post("/transform")
async def transform(
    request: Request,
    recruiter_csv: UploadFile = File(...),
    resume_pdf: UploadFile = File(...),
):

    ########################################################
    # Request ID
    ########################################################

    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.time()

    logger.info(
        f"[{request_id}] Incoming transformation request"
    )

    ########################################################
    # Temporary Directory
    ########################################################

    temp_dir = Path(tempfile.mkdtemp())

    csv_path = temp_dir / recruiter_csv.filename

    resume_path = temp_dir / resume_pdf.filename

    try:

        ####################################################
        # Save Recruiter CSV
        ####################################################

        logger.info(
            f"[{request_id}] Saving recruiter CSV..."
        )

        with open(csv_path, "wb") as buffer:
            shutil.copyfileobj(
                recruiter_csv.file,
                buffer,
            )

        ####################################################
        # Save Resume PDF
        ####################################################

        logger.info(
            f"[{request_id}] Saving resume PDF..."
        )

        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(
                resume_pdf.file,
                buffer,
            )

        ####################################################
        # Execute Pipeline
        ####################################################

        logger.info(
            f"[{request_id}] Executing transformation pipeline..."
        )

        response = pipeline.run(
            csv_path=str(csv_path),
            resume_path=str(resume_path),
        )

        ####################################################
        # Processing Time
        ####################################################

        elapsed = round(
            time.time() - start_time,
            3,
        )

        logger.info(
            f"[{request_id}] Pipeline completed successfully in {elapsed}s"
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

            if csv_path.exists():
                csv_path.unlink()

            if resume_path.exists():
                resume_path.unlink()

            temp_dir.rmdir()

            logger.info(
                f"[{request_id}] Temporary files cleaned"
            )

        except Exception as cleanup_error:

            logger.warning(
                f"[{request_id}] Cleanup failed: {cleanup_error}"
            )