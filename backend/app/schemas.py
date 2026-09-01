from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CategoryScore(BaseModel):
    category: str
    confidence: float


class CategoryPrediction(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    category: str
    confidence: float
    top_categories: list[CategoryScore]
    explanation_terms: list[str]
    model_used: str


class JobFit(BaseModel):
    fit_score: float
    text_similarity_pct: float
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    extra_resume_skills: list[str]
    skill_coverage_pct: float


class AnalyzeResponse(BaseModel):
    filename: str
    word_count: int
    category_prediction: CategoryPrediction
    job_fit: JobFit | None = None


class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    status: str
    model_ready: bool
    categories: list[str]
