"""
Configuration and constants for the Job Search and Application-Preparation Agent.
Strict adherence to temperature = 0.1 and reproducible, high-quality generation.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
JOBS_FILE = DATA_DIR / "jobs.json"
CANDIDATES_FILE = DATA_DIR / "candidates.json"
REPORTS_DIR = BASE_DIR / "reports"

# Core Agent Parameters
AGENT_TEMPERATURE = 0.1  # Strictly 0.1 as specified by user
DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3"

# Domain categories for MBA recruitment
DOMAINS = [
    "Consulting & Strategy",
    "Product Management & Tech",
    "Finance & FinTech",
    "Marketing & Brand Management",
    "Operations & Supply Chain"
]

# Match Scoring Weights
MATCH_WEIGHTS = {
    "skill_overlap": 0.45,
    "semantic_similarity": 0.35,
    "domain_alignment": 0.20
}

