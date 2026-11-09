"""
Matching and Scoring Engine for Candidate Profiles and MBA Job Postings.
Combines exact & fuzzy skill overlap, TF-IDF cosine similarity, and domain alignment.
"""

import re
from typing import Dict, List, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.config import MATCH_WEIGHTS


def normalize_text(text: str) -> str:
    """Normalize text by lowering case and stripping non-alphanumeric chars."""
    return re.sub(r"[^\w\s]", " ", text.lower()).strip()


def extract_skills_set(skills_list: List[str]) -> set:
    """Normalize a list of skills into a normalized lookup set."""
    normalized = set()
    for s in skills_list:
        clean = normalize_text(s)
        if clean:
            normalized.add(clean)
    return normalized


def calculate_skill_overlap(candidate_skills: List[str], job_skills: List[str]) -> Tuple[float, List[str], List[str]]:
    """
    Compute skill overlap ratio and identify matched vs missing skills.
    Returns: (overlap_ratio, matched_skills, missing_skills)
    """
    if not job_skills:
        return 1.0, [], []

    cand_set = extract_skills_set(candidate_skills)
    job_set = extract_skills_set(job_skills)

    matched = []
    missing = []

    for orig_job_skill in job_skills:
        clean_job_skill = normalize_text(orig_job_skill)
        # Check direct or partial inclusion
        is_match = False
        for c_skill in cand_set:
            if clean_job_skill in c_skill or c_skill in clean_job_skill:
                is_match = True
                break
        
        if is_match:
            matched.append(orig_job_skill)
        else:
            missing.append(orig_job_skill)

    overlap_ratio = len(matched) / len(job_skills)
    return round(overlap_ratio, 3), matched, missing


def calculate_semantic_similarity(candidate_text: str, job_text: str) -> float:
    """Compute TF-IDF cosine similarity between candidate profile and job description."""
    if not candidate_text.strip() or not job_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform([candidate_text, job_text])
        score = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        return round(max(0.0, min(1.0, score)), 3)
    except Exception:
        return 0.5


def calculate_domain_alignment(candidate: Dict[str, Any], job: Dict[str, Any]) -> float:
    """Calculate domain alignment between candidate target roles/degree and job domain."""
    score = 0.3  # Base baseline for general MBA
    
    cand_targets = [normalize_text(t) for t in candidate.get("target_roles", [])]
    job_domain = normalize_text(job.get("domain", ""))
    job_title = normalize_text(job.get("title", ""))

    # Check for direct keyword overlap
    for target in cand_targets:
        if any(w in job_domain for w in target.split()) or any(w in job_title for w in target.split()):
            score = 1.0
            return score

    # Check coursework and degree
    cand_degree = normalize_text(candidate.get("degree", ""))
    if any(w in job_domain for w in cand_degree.split()):
        score = max(score, 0.8)

    return round(score, 2)


def score_candidate_for_job(candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute comprehensive matching score and diagnostic breakdown.
    """
    all_cand_skills = candidate.get("skills_hard", []) + candidate.get("skills_soft", [])
    job_req_skills = job.get("required_skills", [])
    job_pref_skills = job.get("preferred_skills", [])

    # Skill overlaps
    req_overlap, matched_req, missing_req = calculate_skill_overlap(all_cand_skills, job_req_skills)
    pref_overlap, matched_pref, missing_pref = calculate_skill_overlap(all_cand_skills, job_pref_skills)

    # Candidate comprehensive profile text
    cand_text = f"""
    {candidate.get('summary', '')}
    Target: {' '.join(candidate.get('target_roles', []))}
    Skills: {' '.join(all_cand_skills)}
    Coursework: {' '.join(candidate.get('coursework', []))}
    Projects: {' '.join(candidate.get('projects', []))}
    """

    # Job description text
    job_text = f"""
    {job.get('title', '')} {job.get('domain', '')} {job.get('description', '')}
    Requirements: {' '.join(job_req_skills)}
    Preferred: {' '.join(job_pref_skills)}
    """

    semantic_score = calculate_semantic_similarity(cand_text, job_text)
    domain_score = calculate_domain_alignment(candidate, job)

    # Blended score with weights
    combined_skill_score = (0.75 * req_overlap) + (0.25 * pref_overlap)
    total_score = (
        MATCH_WEIGHTS["skill_overlap"] * combined_skill_score +
        MATCH_WEIGHTS["semantic_similarity"] * semantic_score +
        MATCH_WEIGHTS["domain_alignment"] * domain_score
    )

    total_score_pct = round(total_score * 100, 1)

    return {
        "job_id": job.get("id"),
        "job_title": job.get("title"),
        "company": job.get("company"),
        "domain": job.get("domain"),
        "location": job.get("location"),
        "match_score_pct": total_score_pct,
        "skill_overlap_ratio": req_overlap,
        "semantic_similarity": semantic_score,
        "domain_alignment": domain_score,
        "matched_required_skills": matched_req,
        "missing_required_skills": missing_req,
        "matched_preferred_skills": matched_pref,
        "missing_preferred_skills": missing_pref
    }

