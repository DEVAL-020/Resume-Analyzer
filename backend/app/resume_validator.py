"""
Checks whether extracted document text actually looks like a resume,
so the analyzer only runs on resumes -- not random PDFs/DOCX/TXT files
someone might upload by mistake (invoices, essays, contracts, etc.).

This is a heuristic, not a classifier: it looks for the structural
signals almost every resume has (section headers like "Experience" /
"Education" / "Skills", a contact-info pattern, and a plausible length)
and requires a minimum number of them before treating the file as a
resume. It intentionally errs toward permissive -- most real resumes
clear the bar easily -- while still catching obviously-unrelated
documents.
"""

from __future__ import annotations

import re

# Section headers that show up in the overwhelming majority of resumes.
# Matched as whole words/phrases, case-insensitive.
SECTION_KEYWORDS = [
    r"experience", r"work history", r"employment history",
    r"education", r"academic background",
    r"skills", r"technical skills", r"core competencies",
    r"summary", r"objective", r"profile",
    r"projects", r"certifications?", r"achievements?",
    r"references", r"qualifications",
]

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d\-\.\s()]{8,}\d)")
SECTION_RE = re.compile(
    r"(?<![a-z])(" + "|".join(SECTION_KEYWORDS) + r")(?![a-z])",
    re.IGNORECASE,
)

MIN_WORD_COUNT = 40
MIN_SIGNAL_SCORE = 2  # need at least this many distinct signals


def resume_confidence(text: str) -> dict:
    """
    Returns a dict describing how "resume-like" the text is:
      { is_resume: bool, score: int, signals: list[str], word_count: int }
    """
    word_count = len(text.split())
    signals: list[str] = []

    section_hits = set(m.lower() for m in SECTION_RE.findall(text))
    if len(section_hits) >= 2:
        signals.append(f"{len(section_hits)} resume section headers found")

    if EMAIL_RE.search(text):
        signals.append("contact email found")

    if PHONE_RE.search(text):
        signals.append("phone number pattern found")

    if word_count >= MIN_WORD_COUNT:
        signals.append("sufficient length")
    else:
        # too short to be a real resume regardless of other signals
        return {
            "is_resume": False,
            "score": 0,
            "signals": [],
            "word_count": word_count,
        }

    score = (
        (1 if len(section_hits) >= 2 else 0)
        + (1 if EMAIL_RE.search(text) else 0)
        + (1 if PHONE_RE.search(text) else 0)
    )

    return {
        "is_resume": score >= MIN_SIGNAL_SCORE,
        "score": score,
        "signals": signals,
        "word_count": word_count,
    }


def is_resume(text: str) -> bool:
    return resume_confidence(text)["is_resume"]
