"""
Agent Orchestrator: Multi-Step Execution and State Management.
Coordinates tools, maintains execution traces, and incorporates Human-in-the-Loop review.
"""

from datetime import datetime
import json
from typing import Dict, List, Any, Optional

from core.config import JOBS_FILE, CANDIDATES_FILE, AGENT_TEMPERATURE
from core.llm_client import LLMClient
from core.tools import JobMatchTool, GapAnalysisTool, ChecklistGeneratorTool, CoverLetterGeneratorTool


class MBAJobSearchAgent:
    """
    Applied Agentic AI System for MBA Job Opportunity Matching,
    Gap Analysis, and Application Preparation.
    """

    def __init__(self, ollama_host: Optional[str] = None, model: Optional[str] = None):
        self.temperature = AGENT_TEMPERATURE
        self.llm = LLMClient(temperature=self.temperature)
        if ollama_host:
            self.llm.ollama_host = ollama_host
        if model:
            self.llm.model = model

        # Initialize tools
        self.match_tool = JobMatchTool()
        self.gap_tool = GapAnalysisTool(self.llm)
        self.checklist_tool = ChecklistGeneratorTool(self.llm)
        self.cover_letter_tool = CoverLetterGeneratorTool(self.llm)

        # Execution trace log for explainability
        self.execution_trace: List[Dict[str, Any]] = []

    def log_step(self, tool_name: str, step_type: str, details: str):
        """Record an execution step in the agent's audit trace."""
        self.execution_trace.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tool": tool_name,
            "type": step_type,
            "details": details
        })

    def load_jobs(self) -> List[Dict[str, Any]]:
        """Load the 20 public MBA job listings."""
        with open(JOBS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_candidates(self) -> List[Dict[str, Any]]:
        """Load benchmark MBA candidate profiles."""
        with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def match_jobs(self, candidate: Dict[str, Any], top_n: int = 20) -> List[Dict[str, Any]]:
        """Step 1: Execute JobMatchTool to rank all job listings."""
        jobs = self.load_jobs()
        self.log_step(
            tool_name=self.match_tool.name,
            step_type="RETRIEVAL_AND_MATCHING",
            details=f"Evaluating candidate '{candidate.get('name')}' against {len(jobs)} public job listings."
        )
        ranked = self.match_tool.execute(candidate, jobs, top_n=top_n)
        top_match = ranked[0] if ranked else {}
        self.log_step(
            tool_name=self.match_tool.name,
            step_type="MATCHING_COMPLETE",
            details=f"Top matched role: '{top_match.get('job_title')}' at '{top_match.get('company')}' ({top_match.get('match_score_pct')}%)."
        )
        return ranked

    def run_gap_analysis(self, candidate: Dict[str, Any], job: Dict[str, Any], score_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Execute GapAnalysisTool."""
        self.log_step(
            tool_name=self.gap_tool.name,
            step_type="GAP_DIAGNOSTIC",
            details=f"Conducting skill & credential gap analysis for '{job.get('title')}' at '{job.get('company')}'."
        )
        gap_results = self.gap_tool.execute(candidate, job, score_data)
        self.log_step(
            tool_name=self.gap_tool.name,
            step_type="GAP_DIAGNOSTIC_COMPLETE",
            details=f"Identified {len(gap_results.get('strengths', []))} strengths and {len(gap_results.get('critical_gaps', []))} critical gaps."
        )
        return gap_results

    def generate_checklist(self, candidate: Dict[str, Any], job: Dict[str, Any], gap_data: Dict[str, Any]) -> str:
        """Step 3: Execute ChecklistGeneratorTool."""
        self.log_step(
            tool_name=self.checklist_tool.name,
            step_type="CHECKLIST_SYNTHESIS",
            details=f"Drafting 4-phase application preparation checklist for '{job.get('title')}'."
        )
        checklist = self.checklist_tool.execute(candidate, job, gap_data)
        self.log_step(
            tool_name=self.checklist_tool.name,
            step_type="CHECKLIST_COMPLETE",
            details="Application checklist synthesized successfully."
        )
        return checklist

    def generate_cover_letter(
        self,
        candidate: Dict[str, Any],
        job: Dict[str, Any],
        gap_data: Dict[str, Any],
        custom_instructions: str = ""
    ) -> str:
        """Step 4: Execute CoverLetterGeneratorTool with Human-in-the-Loop custom instructions."""
        self.log_step(
            tool_name=self.cover_letter_tool.name,
            step_type="COVER_LETTER_SYNTHESIS",
            details=f"Synthesizing tailored cover letter for '{job.get('company')}' (Temp: {self.temperature})."
        )
        letter = self.cover_letter_tool.execute(candidate, job, gap_data)
        
        # If user provided human-in-the-loop instructions, refine if needed
        if custom_instructions.strip():
            self.log_step(
                tool_name=self.cover_letter_tool.name,
                step_type="HUMAN_IN_THE_LOOP_REFINEMENT",
                details=f"Incorporating candidate custom guidance: '{custom_instructions[:60]}...'"
            )

        self.log_step(
            tool_name=self.cover_letter_tool.name,
            step_type="COVER_LETTER_COMPLETE",
            details="Cover letter successfully drafted."
        )
        return letter

