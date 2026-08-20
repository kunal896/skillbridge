"""
rag/ingestion/sample_postings.py

Bundled, offline job-posting dataset used as the ingestion source when
JOB_DATA_PROVIDER has no live API credentials configured (no
ADZUNA_APP_ID / ADZUNA_APP_KEY). This replaces the old 3-posting,
single-role mock in agents/tools.py -- with only 3 generic "Data
Analyst" postings, every target role produced the same citations,
which was a big part of why roadmaps looked identical regardless of
input. This dataset spans several common target roles so retrieval
and roadmap grounding actually vary with the learner's target role and
skill gaps.

Each entry already matches the shape rag.normalization expects:
{job_id, title, company, location, text, source_url, posted_date, role_family}
"""

from typing import Any, Dict, List

SAMPLE_POSTINGS: List[Dict[str, Any]] = [
    # ---- Data Analyst ----
    {
        "job_id": "job_da_001",
        "title": "Junior Data Analyst",
        "company": "TechCorp Logistics",
        "location": "Bengaluru, IN",
        "text": "Seeking a Junior Data Analyst proficient in SQL, PostgreSQL, Excel, and basic Python data manipulation. Responsibilities include running queries, building dashboards, and analyzing customer trends.",
        "source_url": "https://example.com/jobs/job_da_001",
        "posted_date": "2026-08-12",
        "role_family": "Data Analyst",
    },
    {
        "job_id": "job_da_002",
        "title": "Business Intelligence Associate",
        "company": "Northwind Retail",
        "location": "Hyderabad, IN",
        "text": "Looking for a BI associate with strong SQL data aggregation, Tableau/PowerBI experience, and fundamental Python scripting for ETL pipelines and automated reporting.",
        "source_url": "https://example.com/jobs/job_da_002",
        "posted_date": "2026-08-10",
        "role_family": "Data Analyst",
    },
    {
        "job_id": "job_da_003",
        "title": "Data Operations Specialist",
        "company": "Meridian Health",
        "location": "Pune, IN",
        "text": "Key skills required: SQL query optimization, data cleaning with pandas, automated Python scripts, and git version control workflow.",
        "source_url": "https://example.com/jobs/job_da_003",
        "posted_date": "2026-08-05",
        "role_family": "Data Analyst",
    },
    {
        "job_id": "job_da_004",
        "title": "Analytics & Automation Specialist",
        "company": "Vantage Freight",
        "location": "Remote, IN",
        "text": "Build automated ETL pipelines in Python and pandas, design PowerBI dashboards, and integrate LLM-assisted summary reports for weekly operations reviews.",
        "source_url": "https://example.com/jobs/job_da_004",
        "posted_date": "2026-08-16",
        "role_family": "Data Analyst",
    },

    # ---- Backend Engineer ----
    {
        "job_id": "job_be_001",
        "title": "Backend Engineer (Python)",
        "company": "Fintrail Systems",
        "location": "Bengaluru, IN",
        "text": "Design and maintain REST APIs using FastAPI/Django, write PostgreSQL schema migrations, and own service reliability with Docker and CI/CD pipelines.",
        "source_url": "https://example.com/jobs/job_be_001",
        "posted_date": "2026-08-14",
        "role_family": "Backend Engineer",
    },
    {
        "job_id": "job_be_002",
        "title": "Backend Software Engineer",
        "company": "Orbital Payments",
        "location": "Chennai, IN",
        "text": "Strong experience with SQL databases, RESTful API design, authentication/authorization (JWT/OAuth2), and writing unit + integration tests required.",
        "source_url": "https://example.com/jobs/job_be_002",
        "posted_date": "2026-08-09",
        "role_family": "Backend Engineer",
    },
    {
        "job_id": "job_be_003",
        "title": "Platform Engineer - Services Team",
        "company": "Kestrel Cloud",
        "location": "Remote, IN",
        "text": "Own microservices written in Python and Go, manage message queues (Kafka/RabbitMQ), and improve observability with structured logging and metrics.",
        "source_url": "https://example.com/jobs/job_be_003",
        "posted_date": "2026-08-02",
        "role_family": "Backend Engineer",
    },

    # ---- Frontend Engineer ----
    {
        "job_id": "job_fe_001",
        "title": "Frontend Engineer (React)",
        "company": "Lumen Retail",
        "location": "Bengaluru, IN",
        "text": "Build responsive UIs with React, TypeScript, and Tailwind CSS. Collaborate with design on component libraries and improve Core Web Vitals performance.",
        "source_url": "https://example.com/jobs/job_fe_001",
        "posted_date": "2026-08-13",
        "role_family": "Frontend Engineer",
    },
    {
        "job_id": "job_fe_002",
        "title": "UI Engineer - Growth Team",
        "company": "Pixel & Co",
        "location": "Mumbai, IN",
        "text": "Ship pixel-perfect interfaces in Next.js, write accessible semantic HTML, and set up component testing with React Testing Library and Playwright.",
        "source_url": "https://example.com/jobs/job_fe_002",
        "posted_date": "2026-08-07",
        "role_family": "Frontend Engineer",
    },

    # ---- DevOps Engineer ----
    {
        "job_id": "job_do_001",
        "title": "DevOps Engineer",
        "company": "Cascade Infra",
        "location": "Remote, IN",
        "text": "Manage Kubernetes clusters, write Terraform infrastructure-as-code, build CI/CD pipelines (GitHub Actions), and own on-call incident response.",
        "source_url": "https://example.com/jobs/job_do_001",
        "posted_date": "2026-08-11",
        "role_family": "DevOps Engineer",
    },
    {
        "job_id": "job_do_002",
        "title": "Site Reliability Engineer",
        "company": "Northstar Cloud",
        "location": "Pune, IN",
        "text": "Automate infra with Ansible and Terraform, maintain Prometheus/Grafana monitoring, and reduce MTTR through runbook automation and chaos testing.",
        "source_url": "https://example.com/jobs/job_do_002",
        "posted_date": "2026-08-04",
        "role_family": "DevOps Engineer",
    },

    # ---- Machine Learning Engineer ----
    {
        "job_id": "job_ml_001",
        "title": "Machine Learning Engineer",
        "company": "Solace AI",
        "location": "Bengaluru, IN",
        "text": "Train and deploy models with PyTorch/scikit-learn, build feature pipelines, and productionize inference APIs with FastAPI and Docker.",
        "source_url": "https://example.com/jobs/job_ml_001",
        "posted_date": "2026-08-15",
        "role_family": "Machine Learning Engineer",
    },
    {
        "job_id": "job_ml_002",
        "title": "Applied ML Engineer",
        "company": "Verdant Labs",
        "location": "Remote, IN",
        "text": "Work with pandas/numpy for data prep, fine-tune LLMs for classification tasks, and evaluate model performance with rigorous offline metrics.",
        "source_url": "https://example.com/jobs/job_ml_002",
        "posted_date": "2026-08-06",
        "role_family": "Machine Learning Engineer",
    },

    # ---- Product Manager ----
    {
        "job_id": "job_pm_001",
        "title": "Associate Product Manager",
        "company": "Northwind Retail",
        "location": "Hyderabad, IN",
        "text": "Own product discovery with user interviews, write PRDs, run SQL for basic funnel analysis, and prioritize roadmap using RICE scoring.",
        "source_url": "https://example.com/jobs/job_pm_001",
        "posted_date": "2026-08-08",
        "role_family": "Product Manager",
    },
    {
        "job_id": "job_pm_002",
        "title": "Product Manager - Platform",
        "company": "Fintrail Systems",
        "location": "Bengaluru, IN",
        "text": "Partner with engineering on API product decisions, analyze usage with SQL and dashboards, and drive stakeholder alignment across teams.",
        "source_url": "https://example.com/jobs/job_pm_002",
        "posted_date": "2026-08-01",
        "role_family": "Product Manager",
    },

    # ---- QA Engineer ----
    {
        "job_id": "job_qa_001",
        "title": "QA Automation Engineer",
        "company": "Orbital Payments",
        "location": "Chennai, IN",
        "text": "Write automated test suites with Selenium/Playwright and Python, set up CI test pipelines, and design regression test strategy for payment flows.",
        "source_url": "https://example.com/jobs/job_qa_001",
        "posted_date": "2026-08-03",
        "role_family": "QA Engineer",
    },

    # ---- UI/UX Designer ----
    {
        "job_id": "job_ux_001",
        "title": "UI/UX Designer",
        "company": "Pixel & Co",
        "location": "Mumbai, IN",
        "text": "Design user flows and high-fidelity mockups in Figma, run usability testing sessions, and maintain a scalable design system.",
        "source_url": "https://example.com/jobs/job_ux_001",
        "posted_date": "2026-07-30",
        "role_family": "UI/UX Designer",
    },
]
