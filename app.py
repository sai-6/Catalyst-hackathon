import streamlit as st
import os
from agent import run_assessment, generate_questions
from report import generate_pdf

st.set_page_config(page_title="SkillBridge AI", layout="wide", page_icon="🧠")

# --- DATA FROM YOUR README (REINSTATED) ---
DEMO_JD = """We are hiring an HR Executive with strong expertise in:
- Communication and Stakeholder Management
- Conflict Resolution and Mediation
- Employee Engagement and Retention Strategies
- Recruitment and Talent Acquisition
- Emotional Intelligence and Team Dynamics"""

DEMO_RESUME = """MA in Clinical Psychology (2025). 1 year experience as Counselor. 
Skilled in empathy, active listening, and emotional regulation.
Limited corporate HR exposure but strong foundation in human behavior."""

# --- SESSION STATE MANAGEMENT ---
if "jd_input" not in st.session_state: st.session_state.jd_input = ""
if "resume_input" not in st.session_state: st.session_state.resume_input = ""
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None

# --- SIDEBAR (DEMO & NEW ASSESSMENT) ---
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    st.caption("Bridging Psychology into HR")
    
    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.jd_input = ""
        st.session_state.resume_input = ""
        st.session_state.analysis_result = None
        st.rerun()

    if st.button("🎯 Load HR Executive Demo", use_container_width=True):
        st.session_state.jd_input = DEMO_JD
        st.session_state.resume_input = DEMO_RESUME
        st.session_state.analysis_result = None
        st.rerun()

st.title("🧠 SkillBridge AI")
st.markdown("**AI-Powered Skill Assessment & Personalized Learning Agent**")

col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("📄 Job Description", height=250, value=st.session_state.jd_input)
with col2:
    resume = st.text_area("📝 Resume", height=250, value=st.session_state.resume_input)

# Sync state
st.session_state.jd_input = jd
st.session_state.resume_input = resume

if st.button("🔍 Analyze JD & Resume", type="primary", use_container_width=True):
    if not jd.strip() or not resume.strip():
        st.error("Please provide both inputs.")
    else:
        with st.spinner("🧠 Organizational Psychology Engine Running..."):
            result = run_assessment(jd, resume)
            st.session_state.analysis_result = result
            st.rerun()

# --- THE RESULTS ENGINE (RESTORED) ---
if st.session_state.analysis_result:
    res = st.session_state.analysis_result
    st.divider()
    
    col_score, col_pdf = st.columns([3, 1])
    with col_score:
        st.subheader("📊 Assessment Results")
        st.metric("Overall Match Percentage", f"{res.get('match_percentage', 0)}%")
    with col_pdf:
        # PDF Generation Restoration (report.py)
        pdf_file = "SkillBridge_AI_Report.pdf"
        generate_pdf(res, pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download PDF Report", f, file_name=pdf_file, use_container_width=True)

    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Gap Analysis", "📚 Learning Plans"])
    
    with tab1:
        st.write(res.get("summary", ""))
        st.subheader("Key Strengths")
        for strength in res.get("key_strengths", []):
            st.success(strength)
        
    with tab2:
        for item in res.get("detailed_results", []):
            with st.expander(f"**{item.get('skill')}** (Gap: {item.get('gap')})"):
                st.write(f"**Priority:** {item.get('priority')}")
                st.write(f"**Rationale:** {item.get('feedback')}")
                st.info(f"**Interview Question:** {generate_questions(item.get('skill'))}")

    with tab3:
        for item in res.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                st.subheader(f"Strategy for {item.get('skill')}")
                st.markdown(item.get("learning_plan"))

st.caption("Made with ❤️ by Arunjyoti Das | MA Clinical Psychology")
