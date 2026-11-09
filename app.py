"""
Job Search and Application-Preparation Agent for MBA Students.
Course: Applied Agentic AI for Business Applications (BITS Pilani)
Faculty: Dr. Abhishek Verma
Topic 4 Demonstration Application
"""

import streamlit as st
import json
import pandas as pd
from core.agent import MBAJobSearchAgent
from core.config import AGENT_TEMPERATURE, DOMAINS

st.set_page_config(
    page_title="MBA Job Search & Prep Agent | BITS Pilani",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Pastel Theme CSS ────────────────────────────────────────────────────────
PASTEL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ─── Root Variables ─── */
:root {
    --primary: #7C5CFC;
    --primary-light: #A78BFA;
    --primary-bg: #EDE9FE;
    --primary-surface: #F5F3FF;
    --accent-mint: #D1FAE5;
    --accent-mint-text: #065F46;
    --accent-rose: #FFE4E6;
    --accent-rose-text: #9F1239;
    --accent-sky: #DBEAFE;
    --accent-sky-text: #1E40AF;
    --accent-amber: #FEF3C7;
    --accent-amber-text: #92400E;
    --accent-lavender: #EDE9FE;
    --accent-lavender-text: #5B21B6;
    --surface: #FFFFFF;
    --surface-alt: #FAFAFF;
    --text-primary: #1E1B4B;
    --text-secondary: #6B7280;
    --text-muted: #9CA3AF;
    --border: #E5E7EB;
    --border-light: #F3F4F6;
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 20px;
    --radius-xl: 24px;
    --shadow-sm: 0 1px 3px rgba(124,92,252,0.06);
    --shadow-md: 0 4px 16px rgba(124,92,252,0.08);
    --shadow-lg: 0 8px 32px rgba(124,92,252,0.12);
    --shadow-glow: 0 0 24px rgba(124,92,252,0.15);
}

/* ─── Global Resets ─── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #FAFAFF 0%, #F0EDFF 50%, #EDE9FE 100%);
}

/* ─── Sidebar ─── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #7C5CFC 0%, #6D28D9 100%) !important;
    border-right: none !important;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label {
    color: rgba(255,255,255,0.85) !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.02em;
}

section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: var(--radius-sm) !important;
    color: #FFFFFF !important;
    backdrop-filter: blur(8px);
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
}

section[data-testid="stSidebar"] .stAlert {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: var(--radius-sm) !important;
    backdrop-filter: blur(8px);
}

/* ─── Main Header ─── */
.hero-banner {
    background: linear-gradient(135deg, #7C5CFC 0%, #A78BFA 60%, #C4B5FD 100%);
    border-radius: var(--radius-xl);
    padding: 2rem 2.5rem;
    margin-bottom: 1.8rem;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -15%;
    width: 300px;
    height: 300px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: 10%;
    width: 200px;
    height: 200px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}

.hero-banner h1 {
    color: #FFFFFF;
    font-weight: 800;
    font-size: 1.9rem;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.02em;
    position: relative;
    z-index: 1;
}

.hero-banner p {
    color: rgba(255,255,255,0.88);
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
    position: relative;
    z-index: 1;
}

/* ─── Cards ─── */
.pastel-card {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    margin-bottom: 1rem;
}

.pastel-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
    border-color: var(--primary-light);
}

.pastel-card-header {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--primary);
    margin-bottom: 0.6rem;
}

.pastel-card-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.2;
}

.pastel-card-subtitle {
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

/* ─── Profile Header Card ─── */
.profile-header {
    background: linear-gradient(135deg, var(--surface) 0%, var(--primary-surface) 100%);
    border-radius: var(--radius-xl);
    padding: 2rem;
    box-shadow: var(--shadow-md);
    border: 1px solid rgba(124,92,252,0.1);
    margin-bottom: 1.5rem;
}

.profile-name {
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 0.15rem;
    letter-spacing: -0.02em;
}

.profile-degree {
    font-size: 0.95rem;
    color: var(--primary);
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.profile-meta {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 0.6rem;
}

.profile-meta-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.profile-meta-item .icon {
    width: 18px;
    height: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--primary-bg);
    border-radius: 50%;
    font-size: 0.65rem;
}

/* ─── Badges & Pills ─── */
.pill {
    display: inline-flex;
    align-items: center;
    padding: 5px 14px;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 3px 4px 3px 0;
    letter-spacing: 0.01em;
    transition: transform 0.2s;
}

.pill:hover {
    transform: scale(1.05);
}

.pill-purple {
    background: var(--accent-lavender);
    color: var(--accent-lavender-text);
}

.pill-green {
    background: var(--accent-mint);
    color: var(--accent-mint-text);
}

.pill-rose {
    background: var(--accent-rose);
    color: var(--accent-rose-text);
}

.pill-sky {
    background: var(--accent-sky);
    color: var(--accent-sky-text);
}

.pill-amber {
    background: var(--accent-amber);
    color: var(--accent-amber-text);
}

/* ─── Skill Bar ─── */
.skill-bar-container {
    margin-bottom: 0.7rem;
}

.skill-bar-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}

.skill-bar-label span:first-child {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-primary);
}

.skill-bar-label span:last-child {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--primary);
}

.skill-bar-track {
    width: 100%;
    height: 8px;
    background: var(--border-light);
    border-radius: 4px;
    overflow: hidden;
}

.skill-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
    transition: width 0.6s ease-out;
}

/* ─── Job Card ─── */
.job-card {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.8rem;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    position: relative;
    overflow: hidden;
}

.job-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--primary);
    border-radius: 4px 0 0 4px;
    opacity: 0;
    transition: opacity 0.3s;
}

.job-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
    border-color: var(--primary-light);
}

.job-card:hover::before {
    opacity: 1;
}

.job-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.2rem;
}

.job-card-company {
    font-size: 0.88rem;
    color: var(--primary);
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.job-card-meta {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-bottom: 0.8rem;
}

/* ─── Score Ring ─── */
.score-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 68px;
    height: 68px;
    border-radius: 50%;
    background: conic-gradient(var(--primary) calc(var(--score) * 3.6deg), var(--border-light) 0deg);
    position: relative;
}

.score-ring-inner {
    width: 54px;
    height: 54px;
    border-radius: 50%;
    background: var(--surface);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.92rem;
    color: var(--primary);
}

/* ─── Section Title ─── */
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.3rem;
    letter-spacing: -0.01em;
}

.section-subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 1.2rem;
}

/* ─── Stat Cards Row ─── */
.stat-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}

.stat-card {
    flex: 1;
    min-width: 140px;
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.2rem 1rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s;
}

.stat-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

.stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 0.6rem;
}

.stat-icon-purple { background: var(--accent-lavender); }
.stat-icon-green { background: var(--accent-mint); }
.stat-icon-sky { background: var(--accent-sky); }
.stat-icon-amber { background: var(--accent-amber); }
.stat-icon-rose { background: var(--accent-rose); }

.stat-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-primary);
}

.stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.15rem;
}

/* ─── Tabs Styling ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--surface);
    border-radius: var(--radius-md);
    padding: 4px;
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-sm);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 8px 16px !important;
    color: var(--text-secondary) !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.25s !important;
}

.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(124,92,252,0.3) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ─── Buttons ─── */
.stButton > button {
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    border: none !important;
    letter-spacing: 0.01em;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary) 0%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(124,92,252,0.3) !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(124,92,252,0.4) !important;
    transform: translateY(-1px);
}

.stButton > button[kind="secondary"],
.stButton > button:not([kind="primary"]) {
    background: var(--surface) !important;
    color: var(--primary) !important;
    border: 2px solid var(--primary-light) !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button:not([kind="primary"]):hover {
    background: var(--primary-bg) !important;
}

/* ─── Expander ─── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-light) !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* ─── Dataframe ─── */
.stDataFrame {
    border-radius: var(--radius-md) !important;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

/* ─── Text Area ─── */
.stTextArea textarea {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border) !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(124,92,252,0.15) !important;
}

/* ─── Text Input ─── */
.stTextInput input {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
}

.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(124,92,252,0.15) !important;
}

/* ─── Select Box ─── */
.stSelectbox > div > div {
    border-radius: var(--radius-sm) !important;
}

/* ─── Download Buttons ─── */
.stDownloadButton > button {
    border-radius: var(--radius-md) !important;
    background: var(--accent-mint) !important;
    color: var(--accent-mint-text) !important;
    border: none !important;
    font-weight: 600 !important;
}

.stDownloadButton > button:hover {
    background: #A7F3D0 !important;
    transform: translateY(-1px);
}

/* ─── Alerts / Info ─── */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: none !important;
}

/* ─── Link Button ─── */
.stLinkButton a {
    border-radius: var(--radius-md) !important;
    background: linear-gradient(135deg, var(--primary) 0%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    transition: all 0.3s !important;
}

.stLinkButton a:hover {
    box-shadow: 0 4px 14px rgba(124,92,252,0.3) !important;
    transform: translateY(-1px);
}

/* ─── Metric ─── */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1rem;
    box-shadow: var(--shadow-sm);
}

[data-testid="stMetricValue"] {
    color: var(--primary) !important;
    font-weight: 800 !important;
}

/* ─── Comparison Table ─── */
.comparison-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
}

.comparison-table th {
    background: linear-gradient(135deg, var(--primary) 0%, #6D28D9 100%);
    color: #FFFFFF;
    padding: 14px 16px;
    font-weight: 700;
    font-size: 0.85rem;
    text-align: left;
    letter-spacing: 0.02em;
}

.comparison-table td {
    padding: 12px 16px;
    font-size: 0.83rem;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border-light);
    background: var(--surface);
}

.comparison-table tr:nth-child(even) td {
    background: var(--surface-alt);
}

.comparison-table tr:last-child td {
    border-bottom: none;
}

.comparison-table tr:hover td {
    background: var(--primary-surface);
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--primary-light); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* ─── Spinner ─── */
.stSpinner > div {
    border-color: var(--primary) transparent transparent transparent !important;
}

/* ─── Hide default streamlit decorations ─── */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }
</style>
"""
st.markdown(PASTEL_CSS, unsafe_allow_html=True)


# ── Helper: Render skill bar ────────────────────────────────────────────────
def skill_bar(name: str, pct: int):
    return f"""
    <div class="skill-bar-container">
        <div class="skill-bar-label"><span>{name}</span><span>{pct}%</span></div>
        <div class="skill-bar-track"><div class="skill-bar-fill" style="width:{pct}%"></div></div>
    </div>"""


def pills_html(items: list, style: str = "purple") -> str:
    return " ".join(f'<span class="pill pill-{style}">{item}</span>' for item in items)


def stat_card_html(icon: str, value: str, label: str, color: str = "purple") -> str:
    return f"""
    <div class="stat-card">
        <div class="stat-icon stat-icon-{color}">{icon}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
    </div>"""


def score_ring_html(score: float) -> str:
    return f"""
    <div class="score-ring" style="--score:{score}">
        <div class="score-ring-inner">{score}%</div>
    </div>"""


# ── Agent Init ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_agent(ollama_host: str, model_name: str):
    return MBAJobSearchAgent(ollama_host=ollama_host, model=model_name)


# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0 0.6rem;">
        <div style="font-size:1.6rem; font-weight:800; letter-spacing:-0.03em;">🎓 AgentAI</div>
        <div style="font-size:0.78rem; opacity:0.8; margin-top:2px;">BITS Pilani • Department of Management</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### ⚙️ LLM Engine")
    ollama_host = st.text_input("Ollama Endpoint", value="http://localhost:11434")
    model_name = st.text_input("Model", value="llama3")

    agent = get_agent(ollama_host, model_name)
    ollama_online = agent.llm.is_ollama_available()

    if ollama_online:
        st.success(f"🟢 Connected ({model_name})")
    else:
        st.info("🟡 Deterministic Fallback Active")

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.12); border-radius:10px; padding:12px; margin:8px 0;">
        <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; opacity:0.7; margin-bottom:6px;">System Config</div>
        <div style="font-size:0.84rem;">🌡️ Temperature: <b>{AGENT_TEMPERATURE}</b></div>
        <div style="font-size:0.84rem;">💼 Verified Jobs: <b>20</b></div>
        <div style="font-size:0.84rem;">🎯 MBA Sectors: <b>5</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### 👤 Select Candidate")

# Load Data
candidates = agent.load_candidates()
jobs = agent.load_jobs()

with st.sidebar:
    cand_options = {c["name"] + f" ({c['degree'].split(',')[0]})": i for i, c in enumerate(candidates)}
    selected_cand_label = st.selectbox("Choose Profile:", list(cand_options.keys()), label_visibility="collapsed")
    selected_cand_idx = cand_options[selected_cand_label]
    selected_candidate = candidates[selected_cand_idx]


# ── Hero Banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>Applied Agentic AI: MBA Job Search & Prep Agent</h1>
    <p>Topic 4 — Multi-Step Autonomous Opportunity Matching, Gap Analysis, Checklist & Cover Letter Synthesis</p>
</div>
""", unsafe_allow_html=True)


# ── Tabs ────────────────────────────────────────────────────────────────────
tab_profile, tab_catalog, tab_match, tab_gap, tab_prep, tab_inspector = st.tabs([
    "👤 Candidate",
    "💼 Jobs Catalog",
    "🤖 Matcher",
    "🔍 Gap Analysis",
    "📝 Prep & Letter",
    "🔬 Inspection"
])


# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: CANDIDATE PROFILE
# ═══════════════════════════════════════════════════════════════════════════
with tab_profile:
    c = selected_candidate

    # Profile Header Card
    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-name">{c['name']}</div>
        <div class="profile-degree">{c['degree']}</div>
        <div class="profile-meta">
            <div class="profile-meta-item"><span class="icon">🎓</span> {c['undergraduate']}</div>
            <div class="profile-meta-item"><span class="icon">💼</span> {c['years_experience']} years experience</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary
    st.info(f"**Executive Summary:**\n{c['summary']}")

    # Stats row
    st.markdown(f"""
    <div class="stat-row">
        {stat_card_html("🛠️", str(len(c.get('skills_hard', []))), "Hard Skills", "purple")}
        {stat_card_html("🤝", str(len(c.get('skills_soft', []))), "Soft Skills", "sky")}
        {stat_card_html("📜", str(len(c.get('certifications', []))), "Certifications", "amber")}
        {stat_card_html("🎯", str(len(c.get('target_roles', []))), "Target Roles", "green")}
    </div>
    """, unsafe_allow_html=True)

    col_skills, col_details = st.columns([1, 1], gap="large")

    with col_skills:
        # Hard Skills with progress bars
        st.markdown('<div class="section-title">🛠️ Hard & Analytical Skills</div>', unsafe_allow_html=True)
        total_hard = len(c.get('skills_hard', []))
        bars_html = ""
        for idx, s in enumerate(c.get('skills_hard', [])):
            pct = max(55, 100 - idx * 6)  # Decreasing proficiency visualization
            bars_html += skill_bar(s, pct)
        st.markdown(f'<div class="pastel-card">{bars_html}</div>', unsafe_allow_html=True)

        # Soft Skills
        st.markdown('<div class="section-title">🤝 Soft & Leadership Skills</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pastel-card">{pills_html(c.get("skills_soft", []), "sky")}</div>', unsafe_allow_html=True)

    with col_details:
        # Target Roles
        st.markdown('<div class="section-title">🎯 Target Roles</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pastel-card">{pills_html(c.get("target_roles", []), "green")}</div>', unsafe_allow_html=True)

        # Certifications
        st.markdown('<div class="section-title">📜 Certifications</div>', unsafe_allow_html=True)
        certs_html = "".join(f'<div style="padding:6px 0; font-size:0.88rem; color:var(--text-primary);">✦ {cert}</div>' for cert in c.get('certifications', []))
        st.markdown(f'<div class="pastel-card">{certs_html}</div>', unsafe_allow_html=True)

        # Achievements
        st.markdown('<div class="section-title">🏆 Key Honors</div>', unsafe_allow_html=True)
        ach_html = "".join(f'<div style="padding:6px 0; font-size:0.88rem; color:var(--text-primary);">🏅 {a}</div>' for a in c.get('achievements', []))
        st.markdown(f'<div class="pastel-card">{ach_html}</div>', unsafe_allow_html=True)

    # Projects
    st.markdown('<div class="section-title">🚀 Capstone & Live Consulting Projects</div>', unsafe_allow_html=True)
    proj_cols = st.columns(len(c.get('projects', [])))
    for i, proj in enumerate(c.get('projects', [])):
        with proj_cols[i]:
            st.markdown(f"""
            <div class="pastel-card" style="border-left: 4px solid var(--primary);">
                <div style="font-size:0.72rem; font-weight:600; color:var(--primary); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.5rem;">Project {i+1}</div>
                <div style="font-size:0.88rem; color:var(--text-primary); line-height:1.6;">{proj}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: JOB CATALOG
# ═══════════════════════════════════════════════════════════════════════════
with tab_catalog:
    st.markdown('<div class="section-title">Publicly Advertised MBA Job Repository</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">20 verified postings sourced directly from real corporate career portals across 5 MBA career tracks</div>', unsafe_allow_html=True)

    # Stat cards
    domain_counts = {}
    for j in jobs:
        d = j["domain"]
        domain_counts[d] = domain_counts.get(d, 0) + 1

    colors = ["purple", "sky", "green", "amber", "rose"]
    icons = ["📊", "💻", "💰", "📣", "⚙️"]
    stats_html = '<div class="stat-row">'
    for i, (domain, count) in enumerate(domain_counts.items()):
        short_name = domain.split("&")[0].strip()
        stats_html += stat_card_html(icons[i % len(icons)], str(count), short_name, colors[i % len(colors)])
    stats_html += '</div>'
    st.markdown(stats_html, unsafe_allow_html=True)

    # Filters
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        domain_filter = st.selectbox("Filter by Domain:", ["All Domains"] + DOMAINS)
    with f_col2:
        search_query = st.text_input("🔍 Search by Role, Company, or Skill:", "")

    filtered_jobs = jobs
    if domain_filter != "All Domains":
        filtered_jobs = [j for j in filtered_jobs if j["domain"] == domain_filter]
    if search_query:
        q = search_query.lower()
        filtered_jobs = [
            j for j in filtered_jobs
            if q in j["title"].lower() or q in j["company"].lower() or any(q in s.lower() for s in j["required_skills"])
        ]

    st.markdown(f'<div style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:1rem;">Showing <b>{len(filtered_jobs)}</b> positions</div>', unsafe_allow_html=True)

    # Job cards in 2-column grid
    for row_start in range(0, len(filtered_jobs), 2):
        row_jobs = filtered_jobs[row_start:row_start+2]
        cols = st.columns(len(row_jobs))
        for col_idx, j in enumerate(row_jobs):
            with cols[col_idx]:
                # Domain color mapping
                domain_style_map = {
                    "Consulting & Strategy": "purple",
                    "Product Management & Tech": "sky",
                    "Finance & FinTech": "green",
                    "Marketing & Brand Management": "amber",
                    "Operations & Supply Chain": "rose"
                }
                d_style = domain_style_map.get(j['domain'], 'purple')

                skills_pills = pills_html(j['required_skills'][:4], d_style)
                pref_pills = pills_html(j['preferred_skills'][:3], 'purple') if j.get('preferred_skills') else ''

                st.markdown(f"""
                <div class="job-card">
                    <div class="job-card-title">{j['title']}</div>
                    <div class="job-card-company">{j['company']}</div>
                    <div class="job-card-meta">
                        <span>📍 {j['location']}</span>
                        <span>📅 {j['posting_date']}</span>
                        <span>💼 {j['experience_years']}</span>
                    </div>
                    <div style="font-size:0.83rem; color:var(--text-secondary); margin-bottom:0.8rem; line-height:1.5;">{j['description'][:150]}...</div>
                    <div style="margin-bottom:0.5rem;">
                        <div style="font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-muted); margin-bottom:4px;">Required</div>
                        {skills_pills}
                    </div>
                    <div>
                        <div style="font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-muted); margin-bottom:4px;">Preferred</div>
                        {pref_pills}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.link_button(f"View on {j['company']} Careers ↗", j['source_url'], use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 3: AGENTIC MATCHER & RANKING
# ═══════════════════════════════════════════════════════════════════════════
with tab_match:
    st.markdown('<div class="section-title">Autonomous Opportunity Matching & Ranking</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">Evaluating <b>{selected_candidate["name"]}</b> across all 20 jobs using weighted skill overlap, semantic context, and domain alignment</div>', unsafe_allow_html=True)

    if st.button("🚀 Run Agentic Job Matcher", type="primary", use_container_width=True):
        with st.spinner("Agent executing JobMatchTool..."):
            ranked_results = agent.match_jobs(selected_candidate)
            st.session_state["ranked_results"] = ranked_results
            st.session_state["selected_candidate_id"] = selected_candidate["id"]
            st.success(f"✅ Matched and ranked {len(ranked_results)} opportunities!")

    if "ranked_results" in st.session_state and st.session_state.get("selected_candidate_id") == selected_candidate["id"]:
        results = st.session_state["ranked_results"]

        # Top 3 cards
        st.markdown('<div style="margin-top:1rem;"></div>', unsafe_allow_html=True)
        top_cols = st.columns(3)
        medal_icons = ["🥇", "🥈", "🥉"]
        medal_colors = ["amber", "sky", "rose"]

        for i, col in enumerate(top_cols):
            if i < len(results):
                r = results[i]
                with col:
                    st.markdown(f"""
                    <div class="pastel-card" style="text-align:center; border-top:4px solid var(--primary);">
                        <div style="font-size:1.8rem; margin-bottom:0.3rem;">{medal_icons[i]}</div>
                        <div style="font-size:0.72rem; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:0.08em;">Rank #{i+1}</div>
                        <div style="margin:0.8rem auto;">
                            {score_ring_html(r['match_score_pct'])}
                        </div>
                        <div style="font-size:1.05rem; font-weight:700; color:var(--text-primary); margin-bottom:0.15rem;">{r['job_title']}</div>
                        <div style="font-size:0.88rem; color:var(--primary); font-weight:600; margin-bottom:0.5rem;">{r['company']}</div>
                        <div>{pills_html([r['domain']], medal_colors[i])}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Full ranking table
        st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Complete Ranking Table</div>', unsafe_allow_html=True)

        table_data = []
        for rank, r in enumerate(results, 1):
            table_data.append({
                "Rank": rank,
                "Company": r["company"],
                "Job Title": r["job_title"],
                "Domain": r["domain"],
                "Match Score": f"{r['match_score_pct']}%",
                "Skill Overlap": f"{int(r['skill_overlap_ratio']*100)}%",
                "Semantic Similarity": f"{int(r['semantic_similarity']*100)}%",
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

        # Select Target
        st.markdown("---")
        st.markdown('<div class="section-title">Select Target Job for Deep Analysis</div>', unsafe_allow_html=True)

        job_options = {f"#{i+1}: {r['job_title']} @ {r['company']} ({r['match_score_pct']}%)": r for i, r in enumerate(results)}
        selected_job_label = st.selectbox("Select Target Position:", list(job_options.keys()))
        st.session_state["target_score_data"] = job_options[selected_job_label]
        st.session_state["target_job"] = job_options[selected_job_label]["job_details"]

        tj = st.session_state['target_job']
        st.markdown(f"""
        <div class="pastel-card" style="border-left:4px solid var(--primary);">
            <div style="font-size:0.88rem; color:var(--text-secondary);">
                Target selected: <b style="color:var(--text-primary)">{tj['title']}</b> at <b style="color:var(--primary)">{tj['company']}</b>
                — proceed to <b>Gap Analysis</b> tab
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 4: GAP ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
with tab_gap:
    st.markdown('<div class="section-title">Deep Skill Gap & Remediation Diagnostics</div>', unsafe_allow_html=True)

    if "target_job" not in st.session_state:
        st.warning("Please run the Matcher and select a target job in the Matcher tab first!")
    else:
        target_job = st.session_state["target_job"]
        score_data = st.session_state["target_score_data"]

        st.markdown(f"""
        <div class="pastel-card" style="background: linear-gradient(135deg, var(--primary-surface) 0%, var(--surface) 100%);">
            <div style="display:flex; align-items:center; gap:1.5rem; flex-wrap:wrap;">
                <div>
                    {score_ring_html(score_data['match_score_pct'])}
                </div>
                <div>
                    <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">{selected_candidate['name']} → {target_job['title']}</div>
                    <div style="font-size:0.92rem; color:var(--primary); font-weight:600;">{target_job['company']} • {target_job['domain']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔍 Execute Gap Analysis", type="primary", use_container_width=True):
            with st.spinner("Agent running GapAnalysisTool with Temperature = 0.1..."):
                gap_results = agent.run_gap_analysis(selected_candidate, target_job, score_data)
                st.session_state["gap_results"] = gap_results
                st.success("✅ Skill gap analysis and remediation plan synthesized!")

        if "gap_results" in st.session_state:
            gap_data = st.session_state["gap_results"]

            g_col1, g_col2 = st.columns(2, gap="large")

            with g_col1:
                st.markdown("""
                <div class="pastel-card" style="border-top:4px solid #10B981;">
                    <div class="pastel-card-header" style="color:#065F46;">✅ Demonstrated Strengths</div>
                """, unsafe_allow_html=True)
                if gap_data.get("strengths"):
                    st.markdown(pills_html(gap_data["strengths"], "green"), unsafe_allow_html=True)
                else:
                    st.write("No direct required skill matches found.")
                st.markdown('</div>', unsafe_allow_html=True)

            with g_col2:
                st.markdown("""
                <div class="pastel-card" style="border-top:4px solid #F43F5E;">
                    <div class="pastel-card-header" style="color:#9F1239;">⚠️ Critical Skill Gaps</div>
                """, unsafe_allow_html=True)
                if gap_data.get("critical_gaps"):
                    st.markdown(pills_html(gap_data["critical_gaps"], "rose"), unsafe_allow_html=True)
                else:
                    st.write("Zero critical gaps! Candidate meets all required skills.")

                if gap_data.get("minor_gaps"):
                    st.markdown(f"""
                    <div style="margin-top:1rem;">
                        <div style="font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-muted); margin-bottom:6px;">Secondary Gaps</div>
                        {pills_html(gap_data['minor_gaps'], 'amber')}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown('<div class="section-title">📋 Agent Remediation Analysis & Positioning Plan</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="pastel-card">{gap_data.get("remediation_analysis", "")}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 5: CHECKLIST & COVER LETTER
# ═══════════════════════════════════════════════════════════════════════════
with tab_prep:
    st.markdown('<div class="section-title">Application Preparation & Cover Letter</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Human-in-the-Loop review with custom directives and editable outputs</div>', unsafe_allow_html=True)

    if "target_job" not in st.session_state or "gap_results" not in st.session_state:
        st.warning("Please complete Job Matching and Gap Analysis before generating prep artifacts!")
    else:
        target_job = st.session_state["target_job"]
        gap_data = st.session_state["gap_results"]

        st.markdown(f"""
        <div class="pastel-card" style="border-left:4px solid var(--primary);">
            <div style="font-size:0.88rem; color:var(--text-secondary);">
                Target: <b style="color:var(--primary);">{target_job['title']}</b> @ <b>{target_job['company']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # HITL Custom Directives
        with st.expander("🤝 Human-in-the-Loop Custom Directives", expanded=True):
            user_notes = st.text_area(
                "Add personal anecdotes, preferred emphasis, or specific projects to highlight:",
                placeholder="e.g., Emphasize my Capstone project with 14% cost optimization and my leadership in the consulting club.",
                height=100
            )

        col_act1, col_act2 = st.columns(2, gap="medium")
        with col_act1:
            if st.button("📋 Generate Application Checklist", use_container_width=True):
                with st.spinner("Synthesizing actionable 4-phase checklist..."):
                    chk = agent.generate_checklist(selected_candidate, target_job, gap_data)
                    st.session_state["generated_checklist"] = chk
                    st.success("✅ Checklist generated!")

        with col_act2:
            if st.button("✍️ Draft Tailored Cover Letter", type="primary", use_container_width=True):
                with st.spinner("Synthesizing tailored cover letter (Temp = 0.1)..."):
                    cl = agent.generate_cover_letter(selected_candidate, target_job, gap_data, custom_instructions=user_notes)
                    st.session_state["generated_cover_letter"] = cl
                    st.success("✅ Cover letter synthesized!")

        p_col1, p_col2 = st.columns(2, gap="large")

        with p_col1:
            if "generated_checklist" in st.session_state:
                st.markdown("""
                <div class="section-title">📌 4-Phase Application Checklist</div>
                """, unsafe_allow_html=True)
                st.markdown(f'<div class="pastel-card">', unsafe_allow_html=True)
                st.markdown(st.session_state["generated_checklist"])
                st.markdown('</div>', unsafe_allow_html=True)
                st.download_button(
                    "⬇️ Download Checklist (.md)",
                    data=st.session_state["generated_checklist"],
                    file_name=f"Checklist_{target_job['company']}_{selected_candidate['name']}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

        with p_col2:
            if "generated_cover_letter" in st.session_state:
                st.markdown("""
                <div class="section-title">✉️ Tailored Cover Letter</div>
                """, unsafe_allow_html=True)
                edited_cl = st.text_area(
                    "Editable Draft (Human-in-the-Loop Review):",
                    value=st.session_state["generated_cover_letter"],
                    height=450,
                    label_visibility="collapsed"
                )
                st.download_button(
                    "⬇️ Download Cover Letter (.txt)",
                    data=edited_cl,
                    file_name=f"CoverLetter_{target_job['company']}_{selected_candidate['name']}.txt",
                    mime="text/plain",
                    use_container_width=True
                )


# ═══════════════════════════════════════════════════════════════════════════
# TAB 6: INSPECTION & TRACES
# ═══════════════════════════════════════════════════════════════════════════
with tab_inspector:
    st.markdown('<div class="section-title">Agent Audit Trail & Architecture Inspection</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Examining how an AI agent works, uses tools, and differs from basic chatbots</div>', unsafe_allow_html=True)

    # Architecture overview stats
    st.markdown(f"""
    <div class="stat-row">
        {stat_card_html("🔧", "4", "Agent Tools", "purple")}
        {stat_card_html("📊", str(len(agent.execution_trace)), "Trace Entries", "sky")}
        {stat_card_html("🌡️", str(AGENT_TEMPERATURE), "Temperature", "amber")}
        {stat_card_html("🤖", "Multi-Step", "Architecture", "green")}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🔍 Execution Trace Log</div>', unsafe_allow_html=True)
    if agent.execution_trace:
        st.dataframe(pd.DataFrame(agent.execution_trace), use_container_width=True, hide_index=True)
    else:
        st.info("No tool executions logged yet. Run the Matcher, Gap Analyzer, or Generators to populate traces.")

    st.markdown("---")
    st.markdown('<div class="section-title">⚖️ Agent vs. Basic Chatbot</div>', unsafe_allow_html=True)

    comparison_data = [
        ("Goal Orientation", "Reactive single-turn replies", "Proactive multi-step goal execution across job search lifecycle"),
        ("Knowledge Persistence", "Ephemeral context; forgets outside prompt window", "Persistent grounded knowledge base of 20 verified MBA listings & profiles"),
        ("Tool Execution", "Zero native tool execution; hallucinates metrics", "Invokes 4 discrete tools (Match, GapAnalysis, Checklist, CoverLetter)"),
        ("Reasoning Paradigm", "Unconstrained next-token prediction", "Step-by-step state machine with quantitative scoring & diagnostics"),
        ("Output Format", "Unstructured prose; variable quality", "Structured deliverables (checklists, tailored cover letters, audit logs)"),
        ("Human-in-the-Loop", "Passive chat recipient; no feedback loop", "Active human checkpointing: role selection, prompt overrides, draft editing"),
        ("Deterministic Control", "High temperature (~0.7), varying outputs", "Enforced Temperature = 0.1 for grounded, reproducible synthesis"),
    ]

    table_html = '<table class="comparison-table"><thead><tr><th>Dimension</th><th>Standard LLM Chatbot</th><th>Our Job Search Agent</th></tr></thead><tbody>'
    for dim, chatbot, our_agent in comparison_data:
        table_html += f'<tr><td style="font-weight:600; color:var(--primary);">{dim}</td><td>{chatbot}</td><td>{our_agent}</td></tr>'
    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">⚙️ System Prompts & Tool Specification</div>', unsafe_allow_html=True)

    with st.expander("View GapAnalysisTool System Prompt"):
        st.code("You are an elite MBA Career Advisory and Talent Evaluation Agent at a top business school. Analyze candidate gaps against target job requirements with objective rigor, constructive remediation, and professional tone. Keep advice actionable and concise.", language="text")

    with st.expander("View CoverLetterGeneratorTool System Prompt"):
        st.code("You are a professional executive career writer for top MBA candidates. Write a compelling, sophisticated, and tailored cover letter. Strictly avoid fluff and buzzwords. Ground the narrative in concrete evidence from the candidate's actual projects, achievements, and quantified skills. Tone: polished, confident, professional, and forward-looking. Temperature: 0.1.", language="text")
