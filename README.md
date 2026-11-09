# Applied Agentic AI: MBA Job Search & Application-Preparation Agent
**Course:** Applied Agentic AI for Business Applications  
**Institution:** Birla Institute of Technology and Science (BITS), Pilani – Department of Management  
**Faculty In-Charge:** Dr. Abhishek Verma  
**Topic 4:** *Job Search and Application-Preparation Agent: Help an MBA student identify suitable opportunities.*  
**System Sampling Temperature:** `0.1` (Strictly Enforced)

---

## 🌟 Executive Overview
This project delivers a complete, production-grade Agentic AI system that automates the end-to-end recruitment preparation workflow for MBA students. Grounded in the **6 Pillars of Agentic AI**, the agent ingests student resumes, matches them against a verified repository of **20 publicly advertised MBA job listings**, performs a rigorous **Skill & Credential Gap Analysis**, generates an actionable **4-Phase Application Preparation Checklist**, and drafts an evidence-grounded **Tailored Cover Letter** with human-in-the-loop review.

---

## 📁 Project Directory Structure
```
c:\Users\priya\Desktop\BITS Pilani\Sem 3\Deep Learning\
├── data/
│   ├── jobs.json                                # 20 verified public MBA job listings
│   └── candidates.json                          # 4 diverse MBA student candidate archetypes
├── core/
│   ├── __init__.py
│   ├── config.py                                # System settings (Temperature=0.1, Ollama URL, weights)
│   ├── llm_client.py                            # Unified LLM provider (Ollama + Deterministic Fallback)
│   ├── matcher.py                               # Tri-factor mathematical matching engine (TF-IDF + Overlap)
│   ├── tools.py                                 # The 4 Agent tools (Match, Gap, Checklist, CoverLetter)
│   └── agent.py                                 # Agent orchestrator & audit execution trace logger
├── reports/
│   ├── project_report.md                        # Complete project report in Markdown
│   ├── presentation_slides.md                   # 10-slide presentation script with speaker notes
│   └── appendices.md                            # Complete source register, prompts, contribution matrix
├── app.py                                       # Interactive Streamlit Web Prototype
├── generate_documents.py                        # Automated generator for DOCX and PPTX deliverables
├── test_agent.py                                # End-to-end unit and integration test suite
├── Applied_Agentic_AI_Report_Topic4.docx        # 10-12 Page Academic Report (.DOCX)
├── Applied_Agentic_AI_Presentation_Topic4.pptx  # 10 Widescreen 16:9 Presentation Slides (.PPTX)
└── README.md                                    # This documentation
```

---

## 🚀 Quickstart & Demonstration

### 1. Run the Interactive Web Prototype (Streamlit)
To launch the interactive dashboard:
```powershell
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 2. Configure Ollama (Optional)
The agent natively connects to local Ollama instances at `http://localhost:11434` with `temperature = 0.1`:
1. Ensure Ollama is running (`ollama serve`).
2. Pull your preferred model (e.g. `ollama run llama3` or `mistral`).
3. In the Streamlit sidebar, verify that the green indicator displays: `🟢 Ollama Connected (llama3)`.
4. *Note:* If Ollama is offline, the agent automatically activates its built-in deterministic fallback engine, ensuring 100% functionality without interruption!

### 3. Regenerate DOCX Report & PPTX Slides
To re-compile the Microsoft Office submission assets:
```powershell
python generate_documents.py
```
This produces:
- `Applied_Agentic_AI_Report_Topic4.docx` (Academic 10-12 page report)
- `Applied_Agentic_AI_Presentation_Topic4.pptx` (10 widescreen slides with speaker notes)

### 4. Run Automated Test Suite
```powershell
python test_agent.py
```

---

## 🛠️ The 4 Core Agent Tools
1. **`JobMatchTool`**: Computes compatibility across 20 jobs using:
   $$\text{Match Score} = 0.45 \times \text{Skill Overlap} + 0.35 \times \text{Semantic Cosine} + 0.20 \times \text{Domain Alignment}$$
2. **`GapAnalysisTool`**: Isolates Demonstrated Strengths from Critical Deficiencies with a 3-part time-bound upskilling plan.
3. **`ChecklistGeneratorTool`**: Generates a 4-phase preparation roadmap (Resume, Portfolio, Alumni Outreach, Interview Prep).
4. **`CoverLetterGeneratorTool`**: Drafts a customized, 4-paragraph cover letter grounded in candidate capstones under strict Temperature = 0.1.

---

## 🎓 Course Submission Checklist (BITS Pilani)
- [x] **Working Prototype:** Interactive Streamlit web application with live demo capability.
- [x] **Brief Report (10-12 Pages):** Delivered as `Applied_Agentic_AI_Report_Topic4.docx` and `reports/project_report.md`.
- [x] **Presentation Slides (8-10 Slides):** Delivered as `Applied_Agentic_AI_Presentation_Topic4.pptx` (10 slides) and `reports/presentation_slides.md`.
- [x] **Appendices:** Complete 20-job source register, system prompts, test logs, contribution matrix, and AI tools used.
- [x] **Strict Temperature:** Strictly calibrated at `temperature = 0.1`.

