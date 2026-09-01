"""
Layer 2: "job-fit verification" -- does THIS resume actually match THIS
job description, as opposed to layer 1 (predict.py) which only answers
"what general category does this resume look like".

Method
------
1. Clean both texts the same way as training data.
2. Fit a fresh, lightweight TF-IDF vectorizer on just the pair
   [resume, job_description] (this avoids the fixed training vocabulary
   missing JD-specific terms) and compute cosine similarity -> a 0-100
   "text similarity" score.
3. Independently extract skills from both texts against the curated
   skill taxonomy (app/skills.py) -> matched / partially-matched /
   missing skills, and a skill-coverage score.
4. Combine into a single fit_score (weighted average), which is more
   interpretable than TF-IDF similarity alone.
"""

from __future__ import annotations

from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.ml.preprocess import clean_text
from app.skills import extract_jd_skills, extract_skills

# weights for the combined fit score
W_TEXT_SIMILARITY = 0.45
W_SKILL_COVERAGE = 0.55


def text_similarity(resume_text: str, job_description: str) -> float:
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)

    if not resume_clean or not jd_clean:
        return 0.0

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    tfidf = vectorizer.fit_transform([resume_clean, jd_clean])
    sim = cosine_similarity(tfidf[0], tfidf[1])[0][0]
    return float(round(sim * 100, 2))


def skill_match(resume_text: str, job_description: str) -> dict[str, Any]:
    jd_skills = extract_jd_skills(job_description)
    resume_skills = extract_skills(resume_text)

    # also check resume against exactly the JD's custom-extracted tokens
    # (covers skills not in the curated bank, e.g. a specific tool name)
    resume_clean = clean_text(resume_text).lower()
    resume_raw_lower = resume_text.lower()

    matched, missing = set(), set()
    for skill in jd_skills:
        # direct containment check handles both curated + heuristic tokens
        if skill in resume_skills or skill in resume_raw_lower or skill in resume_clean:
            matched.add(skill)
        else:
            missing.add(skill)

    coverage = (len(matched) / len(jd_skills) * 100) if jd_skills else 100.0

    return {
        "required_skills": sorted(jd_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "extra_resume_skills": sorted(resume_skills - jd_skills),
        "skill_coverage_pct": round(coverage, 1),
    }


def compute_fit(resume_text: str, job_description: str) -> dict[str, Any]:
    sim_score = text_similarity(resume_text, job_description)
    skills = skill_match(resume_text, job_description)

    fit_score = round(
        W_TEXT_SIMILARITY * sim_score + W_SKILL_COVERAGE * skills["skill_coverage_pct"],
        1,
    )
    fit_score = max(0.0, min(100.0, fit_score))

    return {
        "fit_score": fit_score,
        "text_similarity_pct": sim_score,
        **skills,
    }
