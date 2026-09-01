from __future__ import annotations

import random
from pathlib import Path

import pandas as pd

random.seed(42)

CATEGORIES: dict[str, list[str]] = {
    "INFORMATION-TECHNOLOGY": [
        "python", "java", "sql", "aws", "docker", "kubernetes", "react",
        "rest api", "git", "linux", "microservices", "ci/cd", "django",
        "machine learning", "cloud computing", "agile", "scrum",
    ],
    "HR": [
        "recruiting", "onboarding", "employee relations", "payroll",
        "talent acquisition", "hris", "performance management",
        "compensation", "benefits administration", "labor relations",
        "conflict resolution", "training and development",
    ],
    "DESIGNER": [
        "photoshop", "illustrator", "figma", "sketch", "indesign",
        "ui design", "ux design", "wireframing", "prototyping",
        "graphic design", "adobe creative suite", "typography", "branding",
    ],
    "TEACHER": [
        "curriculum development", "lesson planning", "classroom management",
        "instructional design", "student assessment", "tutoring",
        "special education", "parent communication", "differentiated instruction",
    ],
    "ADVOCATE": [
        "litigation", "contract review", "legal research", "compliance",
        "legal writing", "westlaw", "case management", "client counseling",
        "negotiation", "regulatory filings",
    ],
    "BUSINESS-DEVELOPMENT": [
        "business development", "lead generation", "crm", "salesforce",
        "negotiation", "account management", "market research",
        "partnership development", "revenue growth", "client relationship",
    ],
    "HEALTHCARE": [
        "patient care", "clinical", "nursing", "hipaa", "emr", "ehr",
        "medical records", "triage", "medication administration",
        "healthcare compliance", "vital signs monitoring",
    ],
    "SALES": [
        "sales", "cold calling", "quota attainment", "crm", "upselling",
        "negotiation", "prospecting", "client relationship",
        "salesforce", "closing deals",
    ],
    "FINANCE": [
        "financial analysis", "budgeting", "forecasting", "excel",
        "financial modeling", "risk management", "investment analysis",
        "variance analysis", "financial reporting",
    ],
    "ENGINEERING": [
        "autocad", "solidworks", "cad", "six sigma", "matlab",
        "process improvement", "project management", "quality control",
        "manufacturing", "root cause analysis",
    ],
    "ACCOUNTANT": [
        "accounting", "bookkeeping", "auditing", "tax", "accounts payable",
        "accounts receivable", "reconciliation", "gaap", "quickbooks",
        "general ledger", "financial statements",
    ],
    "CONSULTANT": [
        "stakeholder management", "process optimization", "strategy",
        "data analysis", "client presentations", "change management",
        "project management", "business case development",
    ],
    "DIGITAL-MEDIA": [
        "seo", "digital marketing", "social media marketing", "content strategy",
        "google analytics", "campaign management", "copywriting",
        "email marketing", "brand strategy",
    ],
    "AVIATION": [
        "flight operations", "faa regulations", "safety compliance",
        "aircraft maintenance", "ground operations", "logistics coordination",
    ],
    "BANKING": [
        "loan processing", "credit analysis", "kyc", "compliance",
        "customer relationship management", "risk assessment", "underwriting",
    ],
    "CONSTRUCTION": [
        "project scheduling", "blueprint reading", "osha compliance",
        "site supervision", "cost estimation", "subcontractor management",
    ],
}

FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Priya", "Wei", "Sofia", "Liam",
               "Neha", "Omar", "Grace", "Ravi", "Emma", "Noah", "Aisha"]
LAST_NAMES = ["Sharma", "Patel", "Johnson", "Garcia", "Kim", "Nguyen",
              "Brown", "Singh", "Lopez", "Chen", "Davis", "Khan"]

DEGREE = ["Bachelor of Science", "Bachelor of Arts", "Master of Science",
          "Bachelor of Engineering", "MBA", "Diploma"]
FIELDS = ["Computer Science", "Business Administration", "Marketing",
          "Mechanical Engineering", "Finance", "Education", "Design",
          "Nursing", "Accounting"]

SUMMARY_TEMPLATES = [
    "Results-driven {role} with {years} years of experience delivering "
    "high-impact outcomes in fast-paced environments.",
    "Motivated {role} professional with a proven track record of "
    "{years} years managing cross-functional initiatives.",
    "Detail-oriented {role} offering {years}+ years of hands-on expertise "
    "and a strong record of measurable results.",
]

ROLE_NAME = {
    "INFORMATION-TECHNOLOGY": "software engineer",
    "HR": "human resources specialist",
    "DESIGNER": "product designer",
    "TEACHER": "educator",
    "ADVOCATE": "legal counsel",
    "BUSINESS-DEVELOPMENT": "business development manager",
    "HEALTHCARE": "healthcare professional",
    "SALES": "sales representative",
    "FINANCE": "finance analyst",
    "ENGINEERING": "mechanical engineer",
    "ACCOUNTANT": "accountant",
    "CONSULTANT": "management consultant",
    "DIGITAL-MEDIA": "digital marketing specialist",
    "AVIATION": "aviation operations coordinator",
    "BANKING": "banking associate",
    "CONSTRUCTION": "construction project manager",
}


def _fake_resume_text(category: str) -> str:
    skills = CATEGORIES[category]
    chosen_skills = random.sample(skills, k=min(len(skills), random.randint(6, 10)))
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    years = random.randint(1, 15)
    role = ROLE_NAME[category]
    summary = random.choice(SUMMARY_TEMPLATES).format(role=role, years=years)
    degree = random.choice(DEGREE)
    field = random.choice(FIELDS)

    experience_lines = []
    for _ in range(random.randint(2, 4)):
        s = random.sample(chosen_skills, k=min(3, len(chosen_skills)))
        experience_lines.append(
            f"Utilized {', '.join(s)} to support key business objectives "
            f"and improve team performance."
        )

    resume = f"""
{name}
Summary
{summary}

Skills
{', '.join(chosen_skills)}

Experience
{chr(10).join(experience_lines)}

Education
{degree} in {field}
""".strip()
    return resume


def _to_html(text: str) -> str:
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    body = "".join(f"<p>{p}</p>" for p in paragraphs)
    return f"<html><body>{body}</body></html>"


def generate(n_per_category: int = 40) -> pd.DataFrame:
    rows = []
    idx = 0
    for category in CATEGORIES:
        for _ in range(n_per_category):
            text = _fake_resume_text(category)
            rows.append(
                {
                    "ID": idx,
                    "Resume_str": text,
                    "Resume_html": _to_html(text),
                    "Category": category,
                }
            )
            idx += 1
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    return df


if __name__ == "__main__":
    out_path = Path(__file__).parent / "sample_resume_data.csv"
    df = generate()
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} synthetic rows across {len(CATEGORIES)} categories -> {out_path}")
