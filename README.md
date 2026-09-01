# AI Resume Analyzer

A two-layer resume analysis tool:

1. **Category prediction** — a TF-IDF + scikit-learn classifier trained on
   thousands of labeled resumes predicts the job category a resume looks
   like it belongs to, and explains itself by surfacing the words that
   drove the prediction.
2. **Job-fit verification** — a separate pass compares the resume directly
   against a specific job description (text similarity + a curated skill
   taxonomy) to produce matched/missing skills and a genuine fit score.

```
ai-resume-analyzer/
├── backend/     FastAPI + scikit-learn/pandas/matplotlib/seaborn ML pipeline
└── frontend/    React + TypeScript + Tailwind CSS (Vite)
```

## Quick start

### 1. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt

# Get training data (see data/README.md for the real Kaggle dataset).
# To try it immediately with a synthetic placeholder dataset instead:
python data/generate_sample_data.py

# Train the model (writes reports/*.png and app/models/*.joblib)
python -m app.ml.train

# Start the API
uvicorn app.main:app --reload --port 8000
```

The API is now live at `http://localhost:8000` (interactive docs at
`http://localhost:8000/docs`).

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env   # points the app at http://localhost:8000
npm run dev
```

Open the printed local URL (typically `http://localhost:5173`).

## Using the real Kaggle dataset

This project is built for the Kaggle
["Resume Dataset" by Snehaan Bhawal](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset).
Download `Resume.csv` and place it at `backend/data/Resume.csv`, then re-run
`python -m app.ml.train` — see `backend/data/README.md` for details. The repo
ships with a synthetic placeholder dataset (same column schema, same
category names) so the pipeline runs end-to-end even without Kaggle access;
swap in the real file for accurate, submission-ready results.

## What's under the hood

**Backend / ML** (`backend/app/`)
- `ml/preprocess.py` — regex + BeautifulSoup text cleaning
- `ml/train.py` — EDA (matplotlib/seaborn plots + summary stats), TF-IDF
  vectorization, cross-validated comparison of Logistic Regression / Linear
  SVM / Naive Bayes / Random Forest, held-out evaluation, confusion matrix
- `ml/predict.py` — loads the trained model and explains predictions via
  per-class coefficient contribution
- `ml/matcher.py` — TF-IDF cosine similarity + skill-taxonomy overlap
  between a resume and a job description
- `skills.py` — curated skill taxonomy spanning the dataset's categories
- `text_extract.py` — PDF (pdfplumber) / DOCX (python-docx) / TXT parsing
- `main.py` — FastAPI routes (`/analyze`, `/match-text`, `/health`)

**Frontend** (`frontend/src/`)
- `components/AnalyzerPanel.tsx` — upload + job description + results
- `components/ScoreGauge.tsx` — hand-built SVG arc gauge for the fit score
- `components/CategoryCard.tsx`, `JobFitCard.tsx`, `SkillChips.tsx` — results
- `lib/api.ts` — typed fetch client for the FastAPI backend

## Reports

After training, `backend/reports/` contains:
- `01_category_distribution.png` — class balance across categories
- `02_resume_length_distribution.png` / `03_length_by_category.png` — descriptive statistics
- `04_summary_statistics.csv` — per-category word-count stats
- `05_top_terms_per_category.png` — top TF-IDF terms per category
- `06_classification_report.txt` / `07_confusion_matrix.png` — held-out evaluation
