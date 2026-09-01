"""
Skill taxonomy + extraction.

This is used by the "job-fit" layer (matcher.py) to explain *why* a resume
does or doesn't match a job description, independently of the ML category
classifier. It's a curated keyword bank spanning the categories present in
the Kaggle 'Resume Dataset' (HR, Designer, Information-Technology, Teacher,
Advocate, Business-Development, Healthcare, Sales, Finance, Engineering,
Accountant, and more), plus general/software skills that show up across
almost every category.

Matching is done on the *cleaned* (lowercased, stopword-stripped) text, so
keys here should be lowercase.
"""

from __future__ import annotations

import re
from typing import Iterable

SKILL_BANK: dict[str, list[str]] = {
    "programming": [
        "python", "java", "javascript", "typescript", "c++", "c#", "sql", "r",
        "go", "golang", "php", "ruby", "swift", "kotlin", "scala", "html",
        "css", "bash", "shell scripting",
    ],
    "data_science_ml": [
        "machine learning", "deep learning", "data science", "pandas",
        "numpy", "scipy", "scikit-learn", "sklearn", "tensorflow", "pytorch",
        "keras", "nlp", "computer vision", "data visualization",
        "matplotlib", "seaborn", "tableau", "power bi", "statistics",
        "regression", "classification", "clustering", "data cleaning",
        "data wrangling", "big data", "spark", "hadoop", "etl",
    ],
    "web_cloud_devops": [
        "react", "angular", "vue", "node.js", "django", "flask", "fastapi",
        "rest api", "graphql", "docker", "kubernetes", "aws", "azure",
        "gcp", "ci/cd", "git", "github", "linux", "microservices",
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "oracle", "sqlite", "redis",
        "database management", "data warehousing", "nosql",
    ],
    "business_finance": [
        "financial analysis", "accounting", "budgeting", "forecasting",
        "bookkeeping", "auditing", "tax", "accounts payable",
        "accounts receivable", "reconciliation", "gaap", "quickbooks",
        "sap", "excel", "financial modeling", "invoicing",
    ],
    "sales_marketing": [
        "sales", "business development", "lead generation", "crm",
        "salesforce", "negotiation", "account management", "marketing",
        "seo", "digital marketing", "social media marketing",
        "market research", "cold calling", "client relationship",
    ],
    "hr": [
        "recruiting", "recruitment", "onboarding", "employee relations",
        "payroll", "talent acquisition", "hris", "performance management",
        "compensation", "benefits administration", "labor relations",
    ],
    "healthcare": [
        "patient care", "clinical", "nursing", "hipaa", "emr", "ehr",
        "medical records", "diagnosis", "phlebotomy", "triage",
        "medication administration", "healthcare compliance",
    ],
    "design": [
        "photoshop", "illustrator", "figma", "sketch", "indesign",
        "ui design", "ux design", "wireframing", "prototyping",
        "graphic design", "adobe creative suite", "typography",
        "branding",
    ],
    "engineering_manufacturing": [
        "autocad", "solidworks", "cad", "six sigma", "lean manufacturing",
        "quality control", "project management", "pmp", "matlab",
        "manufacturing", "supply chain", "process improvement",
    ],
    "legal": [
        "litigation", "contract review", "legal research", "compliance",
        "paralegal", "regulatory", "legal writing", "westlaw",
    ],
    "education": [
        "curriculum development", "lesson planning", "classroom management",
        "instructional design", "student assessment", "tutoring",
    ],
    "soft_skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "time management", "project management", "critical thinking",
        "collaboration", "adaptability", "presentation",
    ],
}

# Flat lookup: skill -> category, and a single sorted list of all skills
# (longest first so multi-word skills like "machine learning" are matched
# before a shorter substring could accidentally win).
ALL_SKILLS: list[str] = sorted(
    {s for group in SKILL_BANK.values() for s in group},
    key=len,
    reverse=True,
)


def _build_pattern(skill: str) -> re.Pattern:
    escaped = re.escape(skill.lower())
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])")


_SKILL_PATTERNS: dict[str, re.Pattern] = {s: _build_pattern(s) for s in ALL_SKILLS}


def extract_skills(text: str, candidates: Iterable[str] | None = None) -> set[str]:
    """
    Return the set of skills (from SKILL_BANK, or a custom `candidates`
    list e.g. skills pulled out of a job description) found in `text`.
    `text` should already be lightly cleaned (lowercase is enforced here
    regardless).
    """
    if not text:
        return set()
    haystack = text.lower()
    pool = candidates if candidates is not None else ALL_SKILLS
    found = set()
    for skill in pool:
        pattern = _SKILL_PATTERNS.get(skill) or _build_pattern(skill)
        if pattern.search(haystack):
            found.add(skill)
    return found


def extract_jd_skills(job_description: str) -> set[str]:
    """
    Pull candidate 'required skills' out of a free-text job description.
    Uses the full skill bank as a vocabulary (a JD only rarely mentions a
    skill that isn't in some standard taxonomy), plus a light heuristic
    that also catches comma/bullet separated tokens near words like
    'required', 'skills', 'proficient in', 'experience with'.
    """
    known = extract_skills(job_description)

    extra = set()
    trigger_pattern = re.compile(
        r"(?:required skills|requirements|skills|proficient in|"
        r"experience with|knowledge of)\s*:?\s*(.+)",
        re.IGNORECASE,
    )
    for match in trigger_pattern.finditer(job_description):
        chunk = match.group(1)
        chunk = chunk.split("\n")[0]
        parts = re.split(r"[,/•\u2022]", chunk)
        for p in parts:
            token = p.strip(" .").lower()
            if 2 <= len(token) <= 30 and re.match(r"^[a-z0-9 +#.]+$", token):
                extra.add(token)

    return known | extra
