"""
Loads the trained TF-IDF + classifier artifacts and exposes:

  predict_category(resume_text) -> {
      category, confidence, top_categories, explanation_terms
  }

Explainability:
  - For linear models (LogisticRegression / LinearSVC) we take the
    per-class coefficient vector, multiply element-wise by the resume's
    TF-IDF vector, and surface the highest-contributing terms -- i.e.
    "these words in your resume are what pushed the prediction toward
    this category".
  - For non-linear models (RandomForest) we fall back to reporting the
    resume's own highest-TF-IDF terms as a proxy explanation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np

from app.ml.preprocess import clean_text

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"

_model = None
_vectorizer = None
_label_encoder = None
_meta: dict[str, Any] = {}


class ModelNotTrainedError(RuntimeError):
    pass


def _load_artifacts() -> None:
    global _model, _vectorizer, _label_encoder, _meta
    if _model is not None:
        return
    required = ["classifier.joblib", "tfidf_vectorizer.joblib",
                "label_encoder.joblib", "meta.joblib"]
    missing = [f for f in required if not (MODELS_DIR / f).exists()]
    if missing:
        raise ModelNotTrainedError(
            "Model artifacts not found: "
            f"{missing}. Run `python -m app.ml.train` from the backend/ "
            "directory first."
        )
    _model = joblib.load(MODELS_DIR / "classifier.joblib")
    _vectorizer = joblib.load(MODELS_DIR / "tfidf_vectorizer.joblib")
    _label_encoder = joblib.load(MODELS_DIR / "label_encoder.joblib")
    _meta = joblib.load(MODELS_DIR / "meta.joblib")


def is_ready() -> bool:
    try:
        _load_artifacts()
        return True
    except ModelNotTrainedError:
        return False


def get_meta() -> dict[str, Any]:
    _load_artifacts()
    return _meta


def _top_terms_linear(vec_row, class_idx: int, top_n: int) -> list[str]:
    coef = _model.coef_[class_idx] if _model.coef_.ndim > 1 else _model.coef_[0]
    dense_row = np.asarray(vec_row.todense()).flatten()
    contribution = dense_row * coef
    top_idx = contribution.argsort()[::-1][:top_n]
    top_idx = [int(i) for i in top_idx if contribution[i] > 0]
    feature_names = _vectorizer.get_feature_names_out()
    return [feature_names[i] for i in top_idx]


def _top_terms_generic(vec_row, top_n: int) -> list[str]:
    dense = np.asarray(vec_row.todense()).flatten()
    top_idx = dense.argsort()[::-1][:top_n]
    top_idx = [int(i) for i in top_idx if dense[i] > 0]
    feature_names = _vectorizer.get_feature_names_out()
    return [feature_names[i] for i in top_idx]


def predict_category(raw_text: str, top_k: int = 3, top_terms: int = 10) -> dict[str, Any]:
    _load_artifacts()

    cleaned = clean_text(raw_text)
    vec_row = _vectorizer.transform([cleaned])

    classes = _label_encoder.classes_

    if hasattr(_model, "predict_proba"):
        proba = _model.predict_proba(vec_row)[0]
    elif hasattr(_model, "decision_function"):
        scores = _model.decision_function(vec_row)[0]
        exp_scores = np.exp(scores - np.max(scores))
        proba = exp_scores / exp_scores.sum()
    else:
        pred_idx = _model.predict(vec_row)[0]
        proba = np.zeros(len(classes))
        proba[pred_idx] = 1.0

    order = np.argsort(proba)[::-1]
    top_categories = [
        {"category": classes[i], "confidence": round(float(proba[i]), 4)}
        for i in order[:top_k]
    ]
    best_idx = int(order[0])
    best_category = classes[best_idx]
    confidence = float(proba[best_idx])

    if hasattr(_model, "coef_"):
        explanation_terms = _top_terms_linear(vec_row, best_idx, top_terms)
    else:
        explanation_terms = _top_terms_generic(vec_row, top_terms)

    return {
        "category": best_category,
        "confidence": round(confidence, 4),
        "top_categories": top_categories,
        "explanation_terms": explanation_terms,
        "model_used": _meta.get("model_name", "unknown"),
    }
