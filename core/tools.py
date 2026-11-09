"""
Agent Tools Suite for MBA Job Search and Application Preparation.
Includes:
- JobMatchTool
- GapAnalysisTool
- ChecklistGeneratorTool
- CoverLetterGeneratorTool
"""

from typing import Dict, List, Any
from core.matcher import score_candidate_for_job
from core.llm_client import LLMClient


class JobMatchTool:
    """Tool 1: Evaluate and rank all job openings for a candidate profile."""

    def __init__(self):
        self.name = "job_matching_tool"
        self.description = "Ranks catalog of jobs against candidate profile using multi-metric alignment."

    def execute(self, candidate: Dict[str, Any], jobs: List[Dict[str, Any]], top_n: int = 20) -> List[Dict[str, Any]]:
        scored_jobs = []
        for job in jobs:
            score_data = score_candidate_for_job(candidate, job)
            score_data["job_details"] = job
            scored_jobs.append(score_data)

        # Sort descending by match score
        scored_jobs.sort(key=lambda x: x["match_score_pct"], reverse=True)
        return scored_jobs[:top_n]


class GapAnalysisTool:
    """Tool 2: Conduct granular skill, experience, and credential gap analysis."""

    def __init__(self, llm_client: LLMClient):
        self.name = "gap_analysis_tool"
        self.description = "Categorizes candidate strengths, partial overlaps, and critical deficiencies with remedies."
        self.llm = llm_client

    def execute(self, candidate: Dict[str, Any], job: Dict[str, Any], score_data: Dict[str, Any]) -> Dict[str, Any]:
        matched_req = score_data.get("matched_required_skills", [])
        missing_req = score_data.get("missing_required_skills", [])
        matched_pref = score_data.get("matched_preferred_skills", [])
        missing_pref = score_data.get("missing_preferred_skills", [])

        # Categorize gaps
        strengths = matched_req + matched_pref
        critical_gaps = missing_req
        minor_gaps = missing_pref

        # Build prompt for LLM synthesis (temperature = 0.1)
        system_prompt = (
            "You are an elite MBA Career Advisory and Talent Evaluation Agent at a top business school. "
            "Analyze candidate gaps against target job requirements with objective rigor, constructive remediation, "
            "and professional tone. Keep advice actionable and concise."
        )

        user_prompt = f"""
Candidate: {candidate.get('name')} ({candidate.get('degree')})
Undergraduate: {candidate.get('undergraduate')}
Prior Experience: {candidate.get('years_experience')} years
Summary: {candidate.get('summary')}

Target Job: {job.get('title')} at {job.get('company')} ({job.get('domain')})
Requirements: {', '.join(job.get('required_skills', []))}
Preferred: {', '.join(job.get('preferred_skills', []))}

Automated Diagnosis:
- Demonstrated Strengths: {', '.join(strengths) if strengths else 'None detected'}
- Critical Deficiencies: {', '.join(critical_gaps) if critical_gaps else 'None'}
- Minor / Preferred Deficiencies: {', '.join(minor_gaps) if minor_gaps else 'None'}

Please provide:
1. Executive Fit Assessment (2-3 sentences evaluating readiness).
2. Actionable Skill Remediation Plan (3 specific courses, tools, or micro-projects the candidate must pursue within 2-4 weeks).
3. Interview Positioning Strategy (how to explain the gaps during behavioral or technical rounds).
"""
        llm_response = self.llm.generate(user_prompt, system_prompt)

        # Fallback structured advice if LLM is offline
        if not llm_response.strip():
            llm_response = (
                f"### Executive Fit Assessment\n"
                f"{candidate.get('name')} demonstrates solid foundational alignment ({score_data.get('match_score_pct')}%) for the {job.get('title')} role at {job.get('company')}. "
                f"Their background in {candidate.get('degree')} and demonstrated mastery in {', '.join(strengths[:3]) if strengths else 'analytical coursework'} provides a competitive springboard, though specific focus is needed on {', '.join(critical_gaps[:2]) if critical_gaps else 'domain nuances'}.\n\n"
                f"### Actionable Skill Remediation Plan\n"
                f"1. **Core Proficiency Build:** Dedicate 15-20 hours to targeted case studies or tools covering {critical_gaps[0] if critical_gaps else 'enterprise roadmapping'}.\n"
                f"2. **Portfolio Evidence:** Build a verifiable 1-page artifact or analytical teardown relevant to {job.get('company')}'s current industry initiatives.\n"
                f"3. **Micro-Credentialing:** Complete an industry-standard certification or masterclass in {minor_gaps[0] if minor_gaps else 'strategic execution'}.\n\n"
                f"### Interview Positioning Strategy\n"
                f"Frame transferable competencies from {candidate.get('summary')[:80]}... as evidence of rapid learning agility. Directly acknowledge {critical_gaps[0] if critical_gaps else 'unfamiliar tools'} by showing ongoing self-directed study and proactive problem solving."
            )

        return {
            "strengths": strengths,
            "critical_gaps": critical_gaps,
            "minor_gaps": minor_gaps,
            "remediation_analysis": llm_response
        }


class ChecklistGeneratorTool:
    """Tool 3: Generate a customized, phase-wise application checklist."""

    def __init__(self, llm_client: LLMClient):
        self.name = "checklist_generator_tool"
        self.description = "Builds an actionable 4-phase preparation and submission checklist."
        self.llm = llm_client

    def execute(self, candidate: Dict[str, Any], job: Dict[str, Any], gap_data: Dict[str, Any]) -> str:
        system_prompt = (
            "You are an expert MBA Placement Coach. Generate a highly structured, actionable 4-phase application preparation checklist "
            "for an MBA student applying to a premier corporate position. Include concrete deliverables and checkboxes."
        )

        user_prompt = f"""
Candidate: {candidate.get('name')}
Target Role: {job.get('title')} at {job.get('company')}
Key Gaps to Address: {', '.join(gap_data.get('critical_gaps', []))}

Generate a 4-phase preparation checklist:
Phase 1: Resume & Profile Customization (specific bullet point adjustments)
Phase 2: Verifiable Work / Portfolio Artifacts (specific case teardown or model)
Phase 3: Targeted Networking & Alumni Outreach (ideal connection profiles and message hook)
Phase 4: Interview & Assessment Center Mastery (critical frameworks, behavioral questions)
"""
        response = self.llm.generate(user_prompt, system_prompt)

        if not response.strip():
            response = f"""
### Phase 1: Resume & Profile Customization (Days 1–2)
- [ ] **Quantify Impact Metrics:** Reframe top 3 resume bullets to highlight quantified business outcomes (e.g., % cost savings, revenue delta, process efficiency).
- [ ] **Keyword Optimization:** Integrate mandatory keywords directly into your skills section: `{', '.join(job.get('required_skills', [])[:4])}`.
- [ ] **Headline Alignment:** Update LinkedIn headline to: *Candidate for MBA | Aspiring {job.get('title')} | Focus on {job.get('domain')}*.

### Phase 2: Verifiable Portfolio & Case Artifacts (Days 3–5)
- [ ] **Industry Teardown Deck:** Build a 3-slide executive brief addressing a strategic challenge currently faced by {job.get('company')}.
- [ ] **Analytical Demonstration:** Prepare a clean GitHub/Google Drive repository showcasing {candidate.get('skills_hard', ['modeling'])[0]} applied to a relevant business case.
- [ ] **Executive One-Pager:** Condense your MBA capstone project into a 1-page executive summary tailored to {job.get('company')}'s business model.

### Phase 3: Targeted Networking & Alumni Outreach (Days 6–9)
- [ ] **Alumni Mapping:** Identify 3 BITS Pilani or undergrad alumni currently working in {job.get('domain')} at {job.get('company')}.
- [ ] **Inquiry Message:** Send personalized outreach requesting a 15-minute informational chat on team culture and day-to-day priorities.
- [ ] **Referral Request:** Following a successful dialogue, share your customized resume and request an internal portal referral.

### Phase 4: Interview & Technical Assessment Prep (Days 10–14)
- [ ] **Core Frameworks Drill:** Review foundational frameworks for {job.get('domain')} (e.g., market entry, unit economics, root-cause analysis).
- [ ] **STAR Behavioral Stories:** Prepare 4 distinct STAR stories illustrating leadership, managing ambiguity, client conflict resolution, and data-backed decisions.
- [ ] **Company Knowledge Deep-Dive:** Read {job.get('company')}'s latest annual report / quarterly investor presentation, noting top strategic bets and CEO priorities.
"""
        return response


class CoverLetterGeneratorTool:
    """Tool 4: Generate a tailored, professional cover letter using Temperature = 0.1."""

    def __init__(self, llm_client: LLMClient):
        self.name = "cover_letter_generator_tool"
        self.description = "Synthesizes a personalized, persuasive cover letter matching candidate value to job specifications."
        self.llm = llm_client

    def execute(self, candidate: Dict[str, Any], job: Dict[str, Any], gap_data: Dict[str, Any]) -> str:
        system_prompt = (
            "You are a professional executive career writer for top MBA candidates. "
            "Write a compelling, sophisticated, and tailored cover letter. Strictly avoid fluff and buzzwords. "
            "Ground the narrative in concrete evidence from the candidate's actual projects, achievements, and quantified skills. "
            "Tone: polished, confident, professional, and forward-looking. Temperature: 0.1."
        )

        user_prompt = f"""
Candidate Details:
- Name: {candidate.get('name')}
- Education: {candidate.get('degree')}, {candidate.get('undergraduate')}
- Prior Experience: {candidate.get('years_experience')} years
- Core Skills: {', '.join(candidate.get('skills_hard', []))}
- Key Projects: {' | '.join(candidate.get('projects', []))}
- Notable Achievements: {' | '.join(candidate.get('achievements', []))}

Target Position:
- Role: {job.get('title')}
- Company: {job.get('company')}
- Domain: {job.get('domain')}
- Location: {job.get('location')}
- Mandatory Requirements: {', '.join(job.get('required_skills', []))}

Key Alignment Strengths: {', '.join(gap_data.get('strengths', [])[:5])}
Gaps to Bridge Strategically: {', '.join(gap_data.get('critical_gaps', [])[:2])}

Generate a formal 4-paragraph cover letter formatted with date, recipient salutation, clear subject line, body paragraphs, and professional sign-off.
"""
        response = self.llm.generate(user_prompt, system_prompt)

        if not response.strip():
            # High-grade deterministic template
            proj_highlight = candidate.get('projects', ['a strategic consulting capstone'])[0]
            achieve_highlight = candidate.get('achievements', ['top academic standing'])[0]
            top_skills = ', '.join(candidate.get('skills_hard', [])[:3])

            response = f"""
**Date:** November 8, 2026

**To:**  
The Campus Talent Acquisition Team  
{job.get('company')}  
{job.get('location')}  

**Subject: Application for {job.get('title')} (Req ID: {job.get('id')})**

Dear Hiring Team,

I am writing to express my enthusiastic candidacy for the {job.get('title')} position at {job.get('company')}. Currently completing my {candidate.get('degree')}, complemented by an undergraduate foundation in {candidate.get('undergraduate')}, I have cultivated a rigorous capability in {top_skills}. Having closely followed {job.get('company')}'s industry leadership in {job.get('domain')}, I am eager to contribute my problem-solving rigor, data fluency, and cross-functional leadership to your team.

My prior background encompasses {candidate.get('years_experience')} years of professional experience, where I developed a habit of translating complex challenges into structured, measurable solutions. During my MBA, I demonstrated this capability through {proj_highlight}. This engagement required deep synthesis across quantitative analysis, stakeholder alignment, and strategic execution—skills directly pertinent to the mandate of {job.get('title')}. Furthermore, my recognition as {achieve_highlight} reflects my commitment to high-impact excellence under demanding deadlines.

In reviewing the requirements for the {job.get('title')} role, I noticed the strong emphasis on {', '.join(job.get('required_skills', [])[:3])}. My academic coursework and hands-on projects have given me solid exposure to these disciplines. While {gap_data.get('critical_gaps', ['certain specialized domain methodologies'])[0] if gap_data.get('critical_gaps') else 'specialized tools'} represents a newer dimension in my career roadmap, my demonstrated agility in rapidly mastering new tools and frameworks ensures that I will become a productive contributor from day one.

{job.get('company')}'s dedication to innovation and excellence strongly resonates with my professional ethos. I welcome the opportunity to discuss how my analytical background, business acumen, and proactive work ethic can create immediate value for your organization. Thank you for your time and consideration.

Sincerely,

**{candidate.get('name')}**  
Candidate for {candidate.get('degree')}  
Birla Institute of Technology and Science, Pilani  
Email: {candidate.get('name', 'candidate').lower().replace(' ', '.')}@pilani.bits-pilani.ac.in
"""
        return response.strip()

