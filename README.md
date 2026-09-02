# AI Resume Analyzer 📃📄

--> I built this as a tool that reads a resume, figures out what kind of job it's suited for, and (if you give it a job description) tells you exactly how well it actually fits that role.

**Live demo:** https://ai-resume-analyzer-dp.vercel.app

---

## What it actually does:

1. **Category prediction.** A TF-IDF vectorizer + a classifier (trained on the Kaggle "Resume Dataset") looks at the resume and predicts what job category it belongs to — IT, HR, Healthcare, Finance, and so on. It also shows *which words* pushed it toward that prediction, so it's not a black box.

2. **Job-fit scoring.** This is the part I actually care about. Paste in a real job description, and the app compares your resume against it directly — text similarity plus a skill-taxonomy overlap — and tells you which required skills are covered and which ones are missing. This is the difference between "this resume looks like an engineer's" and "this resume actually matches the job you're applying to."

There's also a basic content check now — if you upload something that isn't a resume (an invoice, an essay, a random PDF), it gets rejected before it wastes a model prediction on garbage input.

## Tech stack:

**Backend:** Python, FastAPI, scikit-learn, pandas, NumPy, SciPy, matplotlib, seaborn, BeautifulSoup, pdfplumber, python-docx

**Frontend:** React, TypeScript, Tailwind CSS, Vite

**Deployed on:** Render (backend) + Vercel (frontend)

## Project structure:

```
ai-resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── ml/
│   │   │   ├── preprocess.py      
│   │   │   ├── train.py            
│   │   │   ├── predict.py          
│   │   │   └── matcher.py         
│   │   ├── skills.py             
│   │   ├── text_extract.py        
│   │   ├── resume_validator.py   
│   │   └── main.py              
│   ├── data/                     
│   └── reports/                
└── frontend/
    └── src/
        ├── components/            
        └── lib/api.ts             
```

## How You run it in your computer:

You'll need Python 3.11 or 3.12 (newer versions can hit dependency build issues on Windows — I learned this the hard way) and Node.js 18+.

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # source venv/bin/activate on Mac/Linux
pip install -r requirements.txt
```

Get some training data — either the real dataset or a quick synthetic one to test with:

```bash
# Option A: the real Kaggle dataset
# Download Resume.csv from kaggle.com/datasets/snehaanbhawal/resume-dataset
# and place it at backend/data/Resume.csv

# Option B: generate a synthetic placeholder dataset instead
python data/generate_sample_data.py
```

Train the model, then start the API:

```bash
python -m app.ml.train
uvicorn app.main:app --reload --port 8000
```

Check `http://localhost:8000/health`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## What I'd still improve

- The skill taxonomy is a curated keyword list, not learned — it'll miss niche or emerging skills that aren't in the bank yet.
- No auth, no persistence — every analysis is stateless, nothing gets saved.

## License

MIT — see [LICENSE](./LICENSE).
