"""
Text preprocessing utilities for the AI Resume Analyzer.

Uses:
- BeautifulSoup  -> strip the Resume_html column down to plain text
- re (regex)     -> clean punctuation / whitespace / boilerplate
- A small hand-built stopword list, so the project has no external
  NLTK/spaCy corpus download dependency (keeps it self-contained and
  reproducible for grading).
"""

from __future__ import annotations

import re

from bs4 import BeautifulSoup

# A compact English stopword list -- enough for TF-IDF quality without
# pulling in nltk.download(...) at runtime (which needs internet access).
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "did", "do", "does", "doing",
    "down", "during", "each", "few", "for", "from", "further", "had", "has", "have",
    "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how",
    "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more",
    "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s",
    "same", "she", "should", "so", "some", "such", "t", "than", "that", "the",
    "their", "theirs", "them", "themselves", "then", "there", "these", "they",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why",
    "will", "with", "would", "you", "your", "yours", "yourself", "yourselves",
}

_WHITESPACE_RE = re.compile(r"\s+")
_NON_ALPHA_RE = re.compile(r"[^a-zA-Z\s]")
_URL_RE = re.compile(r"http\S+|www\.\S+")
_EMAIL_RE = re.compile(r"\S+@\S+")
_MULTISPACE_RE = re.compile(r" {2,}")


def strip_html(raw_html: str) -> str:
    """Convert a Resume_html cell into plain text using BeautifulSoup."""
    if not raw_html or not isinstance(raw_html, str):
        return ""
    soup = BeautifulSoup(raw_html, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return _WHITESPACE_RE.sub(" ", text).strip()


def clean_text(text: str, remove_stopwords: bool = True) -> str:
    """
    Lowercase, strip URLs/emails/digits/punctuation, collapse whitespace,
    and (optionally) drop stopwords. Returns a clean string ready for
    TF-IDF vectorization.
    """
    if not text:
        return ""

    text = text.lower()
    text = _URL_RE.sub(" ", text)
    text = _EMAIL_RE.sub(" ", text)
    text = _NON_ALPHA_RE.sub(" ", text)
    text = _MULTISPACE_RE.sub(" ", text)
    tokens = text.split()

    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]

    return " ".join(tokens)


def clean_resume_row(resume_str: str, resume_html: str) -> str:
    """
    The Kaggle 'Resume Dataset' gives both a raw text column (Resume_str)
    and an HTML column (Resume_html). Resume_str is occasionally noisier
    (stray whitespace / repeated headers from PDF scraping), so we prefer
    it but fall back to stripping the HTML version when Resume_str is
    missing or too short.
    """
    text = resume_str if isinstance(resume_str, str) else ""
    if len(text.strip()) < 20 and resume_html:
        text = strip_html(resume_html)
    return clean_text(text)
