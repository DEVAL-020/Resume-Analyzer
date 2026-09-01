"""
Train the resume-category classifier.

Pipeline:
  1. Load data/Resume.csv (Kaggle) or fall back to the synthetic sample.
  2. Clean text (regex + BeautifulSoup via preprocess.py).
  3. EDA: category distribution, resume-length distribution, top TF-IDF
     terms per category -- saved as PNGs under reports/.
  4. Vectorize with TF-IDF (scikit-learn).
  5. Train + cross-validate several classifiers (Logistic Regression,
     Linear SVM, Multinomial Naive Bayes, Random Forest) and keep the
     best one by macro-F1.
  6. Save a held-out classification report + confusion matrix plot.
  7. Persist the winning model, the TF-IDF vectorizer, and the label
     encoder to app/models/ with joblib, for the FastAPI app to load.

Run from the `backend/` directory:
    python -m app.ml.train
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")  # headless / server-safe backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, classification_report,
                              f1_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

BACKEND_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_DIR / "data"
MODELS_DIR = BACKEND_DIR / "app" / "models"
REPORTS_DIR = BACKEND_DIR / "reports"

sys.path.insert(0, str(BACKEND_DIR))
from app.ml.preprocess import clean_resume_row  # noqa: E402

sns.set_theme(style="whitegrid")


# --------------------------------------------------------------------------
# 1. Load data
# --------------------------------------------------------------------------
def load_dataset() -> pd.DataFrame:
    real_path = DATA_DIR / "Resume.csv"
    synthetic_path = DATA_DIR / "sample_resume_data.csv"

    if real_path.exists():
        print(f"[data] Using real Kaggle dataset: {real_path.name}")
        df = pd.read_csv(real_path)
    elif synthetic_path.exists():
        print(f"[data] Real Resume.csv not found -- using SYNTHETIC "
              f"placeholder dataset: {synthetic_path.name}")
        print("        (see data/README.md to plug in the real Kaggle CSV)")
        df = pd.read_csv(synthetic_path)
    else:
        print("[data] No dataset found. Generating synthetic placeholder ...")
        sys.path.insert(0, str(DATA_DIR))
        from generate_sample_data import generate  # type: ignore
        df = generate()
        df.to_csv(synthetic_path, index=False)

    required = {"Resume_str", "Category"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required column(s): {missing}")

    df = df.dropna(subset=["Category"]).reset_index(drop=True)
    return df


# --------------------------------------------------------------------------
# 2. Clean text
# --------------------------------------------------------------------------
def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    html_col = df["Resume_html"] if "Resume_html" in df.columns else pd.Series([""] * len(df))
    df = df.copy()
    df["clean_text"] = [
        clean_resume_row(s, h) for s, h in zip(df["Resume_str"], html_col)
    ]
    df["char_len"] = df["Resume_str"].fillna("").str.len()
    df["word_count"] = df["clean_text"].str.split().str.len().fillna(0)
    df = df[df["clean_text"].str.len() > 0].reset_index(drop=True)
    return df


# --------------------------------------------------------------------------
# 3. EDA plots
# --------------------------------------------------------------------------
def run_eda(df: pd.DataFrame) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Category distribution
    plt.figure(figsize=(10, 6))
    order = df["Category"].value_counts().index
    sns.countplot(data=df, y="Category", order=order, hue="Category",
                  palette="viridis", legend=False)
    plt.title("Resume Count by Job Category")
    plt.xlabel("Count")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "01_category_distribution.png", dpi=150)
    plt.close()

    # Resume length distribution (descriptive statistics, per syllabus topic)
    plt.figure(figsize=(8, 5))
    sns.histplot(df["word_count"], bins=30, kde=True, color="teal")
    plt.axvline(df["word_count"].mean(), color="red", linestyle="--",
                label=f"mean = {df['word_count'].mean():.0f}")
    plt.axvline(df["word_count"].median(), color="orange", linestyle="--",
                label=f"median = {df['word_count'].median():.0f}")
    plt.title("Resume Length Distribution (word count, cleaned text)")
    plt.xlabel("Word count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "02_resume_length_distribution.png", dpi=150)
    plt.close()

    # Boxplot of length by category (variation / spread across categories)
    plt.figure(figsize=(10, 7))
    sns.boxplot(data=df, x="word_count", y="Category", hue="Category",
                palette="coolwarm", legend=False)
    plt.title("Resume Length by Category")
    plt.xlabel("Word count")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "03_length_by_category.png", dpi=150)
    plt.close()

    # Summary stats table -> CSV (descriptive statistics deliverable)
    summary = df.groupby("Category")["word_count"].agg(
        ["count", "mean", "std", "min", "median", "max"]
    ).round(1)
    summary.to_csv(REPORTS_DIR / "04_summary_statistics.csv")

    print(f"[eda] Saved plots + summary stats to {REPORTS_DIR}")


def plot_top_terms_per_category(df: pd.DataFrame, top_n: int = 8) -> None:
    """Top TF-IDF terms per category -- gives a human-readable sanity
    check of what the model is learning, and doubles as an explainability
    artifact."""
    vec = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), min_df=2)
    X = vec.fit_transform(df["clean_text"])
    terms = np.array(vec.get_feature_names_out())

    categories = df["Category"].unique()
    n_cols = 3
    n_rows = int(np.ceil(len(categories) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    axes = axes.flatten()

    for i, cat in enumerate(categories):
        mask = (df["Category"] == cat).to_numpy()
        cat_scores = np.asarray(X[mask].mean(axis=0)).flatten()
        top_idx = cat_scores.argsort()[::-1][:top_n]
        ax = axes[i]
        sns.barplot(x=cat_scores[top_idx], y=terms[top_idx], ax=ax,
                    hue=terms[top_idx], palette="mako", legend=False)
        ax.set_title(cat, fontsize=10)
        ax.set_xlabel("")
        ax.set_ylabel("")

    for j in range(len(categories), len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle("Top TF-IDF Terms per Category", fontsize=14)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "05_top_terms_per_category.png", dpi=150)
    plt.close()


# --------------------------------------------------------------------------
# 4-5. Vectorize + train/compare models
# --------------------------------------------------------------------------
def build_candidate_models() -> dict:
    return {
        "logistic_regression": LogisticRegression(
            max_iter=2000, C=5.0, class_weight="balanced"
        ),
        "linear_svm": LinearSVC(C=1.0, class_weight="balanced"),
        "multinomial_nb": MultinomialNB(),
        "random_forest": RandomForestClassifier(
            n_estimators=300, max_depth=None, n_jobs=-1, random_state=42
        ),
    }


def train_and_select(X_train: csr_matrix, y_train: np.ndarray) -> tuple[str, object, dict]:
    candidates = build_candidate_models()
    cv_scores = {}
    print("[train] Cross-validating candidate models (5-fold, macro-F1) ...")
    for name, model in candidates.items():
        start = time.time()
        scores = cross_val_score(
            model, X_train, y_train, cv=5, scoring="f1_macro", n_jobs=-1
        )
        elapsed = time.time() - start
        cv_scores[name] = float(scores.mean())
        print(f"    {name:20s} macro-F1 = {scores.mean():.4f}  (+/- {scores.std():.4f})"
              f"   [{elapsed:.1f}s]")

    best_name = max(cv_scores, key=cv_scores.get)
    print(f"[train] Best model by CV macro-F1: {best_name} ({cv_scores[best_name]:.4f})")
    best_model = candidates[best_name]
    best_model.fit(X_train, y_train)
    return best_name, best_model, cv_scores


# --------------------------------------------------------------------------
# 6. Evaluation
# --------------------------------------------------------------------------
def evaluate(model, X_test, y_test, label_encoder: LabelEncoder) -> None:
    y_pred = model.predict(X_test)
    report = classification_report(
        y_test, y_pred, target_names=label_encoder.classes_, zero_division=0
    )
    print("\n[eval] Held-out classification report:\n")
    print(report)

    (REPORTS_DIR / "06_classification_report.txt").write_text(report)

    macro_f1 = f1_score(y_test, y_pred, average="macro")
    print(f"[eval] Held-out macro-F1: {macro_f1:.4f}")

    fig, ax = plt.subplots(figsize=(10, 10))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=label_encoder.classes_,
        xticks_rotation=90, ax=ax, colorbar=False, cmap="Blues",
    )
    ax.set_title("Confusion Matrix -- Resume Category Classifier")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "07_confusion_matrix.png", dpi=150)
    plt.close()


# --------------------------------------------------------------------------
# 7. Persist artifacts
# --------------------------------------------------------------------------
def save_artifacts(model, vectorizer, label_encoder, model_name: str, cv_scores: dict) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "classifier.joblib")
    joblib.dump(vectorizer, MODELS_DIR / "tfidf_vectorizer.joblib")
    joblib.dump(label_encoder, MODELS_DIR / "label_encoder.joblib")
    meta = {
        "model_name": model_name,
        "cv_scores": cv_scores,
        "categories": list(label_encoder.classes_),
    }
    joblib.dump(meta, MODELS_DIR / "meta.joblib")
    print(f"[save] Model artifacts written to {MODELS_DIR}")


def main() -> None:
    df = load_dataset()
    print(f"[data] Loaded {len(df)} rows, {df['Category'].nunique()} categories")

    df = preprocess_dataframe(df)
    run_eda(df)
    plot_top_terms_per_category(df)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["Category"])

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df["clean_text"], y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(
        max_features=8000, ngram_range=(1, 2), min_df=2, sublinear_tf=True
    )
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)

    best_name, best_model, cv_scores = train_and_select(X_train, y_train)
    evaluate(best_model, X_test, y_test, label_encoder)
    save_artifacts(best_model, vectorizer, label_encoder, best_name, cv_scores)


if __name__ == "__main__":
    main()
