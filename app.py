import streamlit as st
import json
import os
from agent import run_assessment, generate_questions
from report import generate_pdf

st.set_page_config(page_title="SkillBridge AI", layout="wide", page_icon="🧠")

# --- COMPLETE DEMO DATA ---
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

DEMO_ANALYSIS_RESULT = {
    "match_percentage": 68,
    "summary": "Strong psychological foundation with excellent emotional intelligence and conflict resolution skills from counseling experience. Needs corporate HR exposure in recruitment, stakeholder management, and employee engagement strategies.",
    "key_strengths": [
        "Exceptional emotional intelligence from clinical psychology background",
        "Proven conflict resolution skills from counseling practice",
        "Strong empathy and active listening abilities",
        "Solid foundation in human behavior analysis"
    ],
    "detailed_results": [
        {"skill": "Emotional Intelligence", "gap": 10, "feedback": "Excellent foundation.", "learning_plan": "1. Read 'Emotional Intelligence 2.0'"},
        {"skill": "Conflict Resolution", "gap": 15, "feedback": "Strong mediation skills.", "learning_plan": "1. Harvard 'Negotiation Mastery'"},
        {"skill": "Communication", "gap": 25, "feedback": "Needs corporate practice.", "learning_plan": "1. Toastmasters workshop"},
        {"skill": "Employee Engagement", "gap": 45, "feedback": "Lacks retention strategy.", "learning_plan": "1. Gallup courses"},
        {"skill": "Recruitment", "gap": 60, "feedback": "No corporate hiring experience.", "learning_plan": "1. LinkedIn Recruiter cert"}
    ]
}

DEMO_USER_ANSWERS = {
    "Emotional Intelligence": "I have developed strong emotional intelligence through my counseling work...",
    "Conflict Resolution": "In counseling, I mediated emotional conflicts between family members...",
    "Communication": "I communicate clearly and empathetically with clients in therapy...",
    "Employee Engagement": "I understand motivation theories and can apply them to retention...",
    "Recruitment": "Limited experience but skilled in psychological assessment."
}

# --- SESSION STATE INITIALIZATION ---
if "jd_input" not in st.session_state:
    st.session_state.jd_input = ""
if "resume_input" not in st.session_state:
    st.session_state.resume_input = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# API Check
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not configured.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    st.caption("Psychology-powered Skill Gap Analysis")

    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.jd_input = ""
        st.session_state.resume_input = ""
        st.session_state.analysis_result = None  # Ensure this is None
        st.session_state.user_answers = {}
        st.rerun()

    if st.button("🎯 Load HR Executive Demo", use_container_width=True):
        # Update session state keys directly to force widget update
        st.session_state.jd_input = DEMO_JD
        st.session_state.resume_input = DEMO_RESUME
        st.session_state.analysis_result = DEMO_ANALYSIS_RESULT
        st.session_state.user_answers = DEMO_USER_ANSWERS
        st.rerun()

# --- MAIN UI ---
st.title("🧠 SkillBridge AI")
st.markdown("**AI-Powered Skill Assessment • Gap Analysis • Personalized Learning Plans**")

col1, col2 = st.columns(2)
with col1:
    # Use key directly to link to session state
    jd = st.text_area("📄 Job Description", height=220, key="jd_input")
with col2:
    resume = st.text_area("📝 Resume", height=220, key="resume_input")

if st.button("🔍 Analyze JD & Resume", type="primary", use_container_width=True):
    if not jd.strip() or not resume.strip():
        st.error("Please provide both JD and Resume.")
    else:
        with st.spinner("Analyzing..."):
            result = run_assessment(jd, resume, {})
            st.session_state.analysis_result = result
            st.success("✅ Analysis Complete!")
            st.rerun()

# --- SHOW RESULTS ---
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "🔍 Skill Breakdown", "❓ Assessment", "📚 Learning Plans"])

    with tab1:
        st.metric("Match Percentage", f"{result.get('match_percentage', 0)}%")
        st.progress(result.get('match_percentage', 0) / 100)
        st.write(result.get("summary", ""))
        st.subheader("Key Strengths")
        for s in result.get("key_strengths", []):
            st.success(s)

    with tab2:
        for item in result.get("detailed_results", []):
            with st.expander(f"{item.get('skill', '')} - Gap: {item.get('gap', 0)}%"):
                st.write(f"**Feedback:** {item.get('feedback', '')}")

    with tab3:
        st.info("Sample answers are pre-filled for demo purposes.")
        for item in result.get("detailed_results", []):
            skill = item.get("skill", "")
            st.subheader(skill)
            # Display question from agent
            st.info(generate_questions(skill))
            # Pre-fill answer area based on demo data or user input
            ans_val = st.session_state.user_answers.get(skill, "")
            st.text_area(f"Your Response ({skill})", value=ans_val, height=100, key=f"ans_{skill}")

    with tab4:
        for item in result.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                with st.expander(f"📚 Learning Plan: {item.get('skill', '')}"):
                    st.markdown(item.get("learning_plan", ""))

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate PDF Report"):
            pdf_path = generate_pdf(result)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, "SkillBridge_Report.pdf", mime="application/pdf")

st.caption("SkillBridge AI — Built by Arunjyoti Das | MA Clinical Psychology")
