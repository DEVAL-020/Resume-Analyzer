from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.ml import matcher
from app.ml.predict import ModelNotTrainedError, get_meta, is_ready, predict_category
from app.resume_validator import resume_confidence
from app.schemas import AnalyzeResponse, HealthResponse
from app.text_extract import UnsupportedFileType, extract_text

MAX_FILE_MB = 8

app = FastAPI(
    title="AI Resume Analyzer API",
    description="Two-layer resume analysis: ML category prediction + job-description fit scoring.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _validate_upload(file: UploadFile, data: bytes) -> None:
    if len(data) == 0:
        raise HTTPException(400, "Uploaded file is empty.")
    if len(data) > MAX_FILE_MB * 1024 * 1024:
        raise HTTPException(400, f"File exceeds {MAX_FILE_MB} MB limit.")
    allowed_ext = (".pdf", ".docx", ".txt")
    if not file.filename or not file.filename.lower().endswith(allowed_ext):
        raise HTTPException(400, "Only PDF, DOCX, or TXT resumes are accepted.")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    ready = is_ready()
    categories = get_meta().get("categories", []) if ready else []
    return HealthResponse(status="ok", model_ready=ready, categories=categories)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str | None = Form(default=None),
) -> AnalyzeResponse:
    data = await resume.read()
    _validate_upload(resume, data)

    try:
        raw_text = extract_text(resume.filename, data)
    except UnsupportedFileType as e:
        raise HTTPException(400, str(e)) from e

    if not raw_text or len(raw_text.strip()) < 30:
        raise HTTPException(
            422,
            "Could not extract meaningful text from this file. "
            "If it's a scanned/image-based PDF, please upload a text-based "
            "resume instead.",
        )

    resume_check = resume_confidence(raw_text)
    if not resume_check["is_resume"]:
        raise HTTPException(
            422,
            "This file doesn't look like a resume (no recognizable sections "
            "like Experience, Education, or Skills, and/or no contact info "
            "were found). Please upload an actual resume in PDF, DOCX, or "
            "TXT format.",
        )

    try:
        category_result = predict_category(raw_text)
    except ModelNotTrainedError as e:
        raise HTTPException(503, str(e)) from e

    job_fit = None
    if job_description and len(job_description.strip()) >= 20:
        job_fit = matcher.compute_fit(raw_text, job_description)

    return AnalyzeResponse(
        filename=resume.filename,
        word_count=len(raw_text.split()),
        category_prediction=category_result,
        job_fit=job_fit,
    )


@app.post("/match-text")
async def match_text(resume_text: str = Form(...), job_description: str = Form(...)):
    """Convenience endpoint for matching raw pasted text (no file upload)."""
    if len(resume_text.strip()) < 30:
        raise HTTPException(422, "resume_text is too short to analyze.")
    if len(job_description.strip()) < 20:
        raise HTTPException(422, "job_description is too short to analyze.")

    resume_check = resume_confidence(resume_text)
    if not resume_check["is_resume"]:
        raise HTTPException(
            422,
            "This text doesn't look like a resume (no recognizable sections "
            "like Experience, Education, or Skills, and/or no contact info "
            "were found). Please paste an actual resume.",
        )

    try:
        category_result = predict_category(resume_text)
    except ModelNotTrainedError as e:
        raise HTTPException(503, str(e)) from e

    job_fit = matcher.compute_fit(resume_text, job_description)
    return {
        "word_count": len(resume_text.split()),
        "category_prediction": category_result,
        "job_fit": job_fit,
    }
