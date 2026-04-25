import streamlit as st
import json
import os
from agent import run_assessment, generate_questions
from report import generate_pdf

st.set_page_config(page_title="SkillBridge AI", layout="wide", page_icon="🧠")

# Demo Data - TOP LEVEL (loaded first)
DEMO_JD = """We are hiring an HR Executive with strong expertise in:
- Communication and Stakeholder Management
- Conflict Resolution and Mediation
- Employee Engagement and Retention Strategies
- Recruitment and Talent Acquisition
- Emotional Intelligence and Team Dynamics"""

DEMO_RESUME = """MA in Clinical Psychology (2025). 
1 year experience as Counselor in rehabilitation setting. 
Skilled in empathy, active listening, emotional regulation, and supporting individuals through difficult situations. 
Limited corporate HR exposure but strong foundation in human behavior and psychology."""

DEMO_ANALYSIS = {
    "match_percentage": 68,
    "summary": "Strong psychological foundation with excellent EI and conflict skills. Needs corporate HR exposure.",
    "key_strengths": [
        "Exceptional emotional intelligence from clinical psychology",
        "Proven conflict resolution from counseling", 
        "Strong empathy and active listening",
        "Solid human behavior foundation"
    ],
    "detailed_results": [
        {"skill": "Emotional Intelligence", "gap": 10, "feedback": "Excellent foundation from counseling.", "learning_plan": "1. EQ 2.0 book\n2. LinkedIn Learning"},
        {"skill": "Conflict Resolution", "gap": 15, "feedback": "Strong mediation skills.", "learning_plan": "1. Negotiation Mastery\n2. Workplace case studies"},
        {"skill": "Communication", "gap": 25, "feedback": "Empathetic but needs corporate practice.", "learning_plan": "1. Toastmasters\n2. Strategic Communication"},
        {"skill": "Employee Engagement", "gap": 45, "feedback": "Psychology applicable, lacks corporate exp.", "learning_plan": "1. Gallup courses\n2. Retention studies"},
        {"skill": "Recruitment", "gap": 60, "feedback": "No corporate exp, strong assessment skills.", "learning_plan": "1. LinkedIn Recruiter cert\n2. ATS training"}
    ]
}

DEMO_ANSWERS = {
    "Emotional Intelligence": "Strong EI from counseling - read emotional cues, help regulate emotions in difficult sessions.",
    "Conflict Resolution": "Mediated family conflicts effectively, de-escalated high-tension situations.",
    "Communication": "Clear empathetic communication with diverse clients, strong active listening.",
    "Employee Engagement": "Understand motivation theories, need corporate retention context.",
    "Recruitment": "Psych assessment skills, eager to learn corporate hiring/ATS."
}

# Session State
if 'demo_active' not in st.session_state:
    st.session_state.demo_active = False
if 'jd' not in st.session_state:
    st.session_state.jd = ""
if 'resume' not in st.session_state:
    st.session_state.resume = ""
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

# API Check
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not configured.")
    st.stop()

# Sidebar - FIXED BUTTON LOGIC
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        if st.button("🆕 New", use_container_width=True):
            st.session_state.demo_active = False
            st.session_state.jd = ""
            st.session_state.resume = ""
            st.session_state.analysis_result = None
            st.session_state.user_answers = {}
            st.rerun()
    
    with col_sb2:
        if st.button("🎯 Demo", use_container_width=True):
            st.session_state.demo_active = True
            st.session_state.jd = DEMO_JD
            st.session_state.resume = DEMO_RESUME
            st.session_state.analysis_result = DEMO_ANALYSIS
            st.session_state.user_answers = DEMO_ANSWERS
            st.rerun()

# MAIN APP - SIMPLIFIED INPUTS
st.title("🧠 SkillBridge AI")
st.markdown("**AI-Powered Skill Assessment • Gap Analysis • Learning Plans**")

# FORCE DISPLAY DEMO DATA FIRST
if st.session_state.demo_active:
    st.session_state.jd = DEMO_JD
    st.session_state.resume = DEMO_RESUME
    st.session_state.analysis_result = DEMO_ANALYSIS
    st.session_state.user_answers = DEMO_ANSWERS

col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("📄 Job Description", value=st.session_state.jd, height=250, key="jd_main")
with col2:
    resume = st.text_area("📝 Resume", value=st.session_state.resume, height=250, key="resume_main")

st.session_state.jd = jd
st.session_state.resume = resume

# Analyze Button
if st.button("🔍 Analyze", type="primary", use_container_width=True):
    if jd.strip() and resume.strip():
        with st.spinner("Analyzing..."):
            result = run_assessment(jd, resume, {})
            st.session_state.analysis_result = result
        st.success("✅ Analysis Complete!")
    else:
        st.error("Please fill both fields")

# RESULTS - FULLY FUNCTIONAL
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "🔍 Skills", "❓ Assessment", "📚 Learning"])
    
    with tab1:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Match %", f"{result.get('match_percentage', 0)}%")
            st.progress(result.get('match_percentage', 0) / 100)
        with col_m2:
            st.markdown(f"**{result.get('summary', '')}**")
        
        st.subheader("✅ Key Strengths")
        for strength in result.get("key_strengths", []):
            st.success(f"• {strength}")

    with tab2:
        for skill_data in result.get("detailed_results", []):
            with st.expander(f"{skill_data.get('skill')} | Gap: {skill_data.get('gap')}%"):
                st.info(skill_data.get('feedback', ''))

    with tab3:
        st.info("💡 Demo includes sample answers")
        for skill_data in result.get("detailed_results", []):
            skill = skill_data['skill']
            st.markdown(f"### {skill}")
            st.markdown("**Questions:**")
            st.write(generate_questions(skill))
            st.markdown("**Sample Answer:**")
            st.text_area("", value=st.session_state.user_answers.get(skill, ""), 
                        height=100, disabled=True, key=f"demo_ans_{skill}")

    with tab4:
        st.markdown("**Personalized Learning Plans**")
        for skill_data in result.get("detailed_results", []):
            if skill_data.get('gap', 0) > 0:
                with st.expander(f"🎯 {skill_data.get('skill')} ({skill_data.get('gap')}%)"):
                    st.markdown(skill_data.get('learning_plan', ''))

    # PDF Export
    st.divider()
    if st.button("📥 Download PDF Report", use_container_width=True):
        pdf_path = generate_pdf(result)
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ PDF Ready", f, "SkillBridge_Report.pdf", "application/pdf")

st.caption("🧠 SkillBridge AI by Arunjyoti Das | Fixed & Production Ready")
