import streamlit as st
import json
import os
from agent import run_assessment, generate_questions
from report import generate_pdf

st.set_page_config(page_title="SkillBridge AI", layout="wide", page_icon="🧠")

# Session State
if "jd" not in st.session_state:
    st.session_state.jd = ""
if "resume" not in st.session_state:
    st.session_state.resume = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# API Check
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not configured.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    st.caption("Psychology-powered Skill Gap Analysis")

    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if st.button("🎯 Load HR Executive Demo", use_container_width=True):
        st.session_state.jd = """We are hiring an HR Executive with strong expertise in:
- Communication and Stakeholder Management
- Conflict Resolution and Mediation
- Employee Engagement and Retention Strategies
- Recruitment and Talent Acquisition
- Emotional Intelligence and Team Dynamics"""

        st.session_state.resume = """MA in Clinical Psychology (2025). 
1 year experience as Counselor in rehabilitation setting. 
Skilled in empathy, active listening, emotional regulation, and supporting individuals through difficult situations. 
Limited corporate HR exposure but strong foundation in human behavior and psychology."""

        # Auto-run analysis for demo
        with st.spinner("Loading demo and running analysis..."):
            result = run_assessment(st.session_state.jd, st.session_state.resume, {})
            st.session_state.analysis_result = result
            
            # Pre-fill some sample answers so video looks complete
            st.session_state.user_answers = {
                "Emotional Intelligence": "I have developed strong emotional intelligence through my counseling work, helping clients regulate emotions during difficult sessions.",
                "Conflict Resolution": "In counseling, I mediated emotional conflicts between family members and clients effectively.",
                "Communication": "I communicate clearly and empathetically with clients from diverse backgrounds in therapy sessions."
            }
        
        st.success("✅ Demo Loaded & Analysis Completed!")
        st.rerun()

# Main UI
st.title("🧠 SkillBridge AI")
st.markdown("**AI-Powered Skill Assessment • Gap Analysis • Personalized Learning Plans**")

col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("📄 Job Description", value=st.session_state.jd, height=220, key="jd_input")
with col2:
    resume = st.text_area("📝 Resume", value=st.session_state.resume, height=220, key="resume_input")

st.session_state.jd = jd
st.session_state.resume = resume

if st.button("🔍 Analyze JD & Resume", type="primary", use_container_width=True):
    if not jd.strip() or not resume.strip():
        st.error("Please provide both JD and Resume.")
    else:
        with st.spinner("Analyzing..."):
            result = run_assessment(jd, resume, {})
            st.session_state.analysis_result = result
            st.success("✅ Analysis Complete!")
            st.rerun()

# Show Results
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
            with st.expander(f"{item.get('skill', '')} - Gap: {item.get('gap', 0)}"):
                st.write(f"**Feedback:** {item.get('feedback', '')}")

    with tab3:
        st.info("Sample answers are pre-filled for demo purposes.")
        for item in result.get("detailed_results", []):
            skill = item.get("skill", "")
            st.subheader(skill)
            st.write(generate_questions(skill))
            st.text_area("Sample Answer (pre-filled)", 
                        value=st.session_state.user_answers.get(skill, ""), 
                        disabled=True, height=80)

    with tab4:
        for item in result.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                with st.expander(f"Learning Plan: {item.get('skill', '')}"):
                    st.markdown(item.get("learning_plan", ""))

    # Export
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate PDF Report"):
            pdf_path = generate_pdf(result)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, "SkillBridge_Report.pdf", mime="application/pdf")

st.caption("SkillBridge AI — Built by Arunjyoti Das | MA Clinical Psychology")
