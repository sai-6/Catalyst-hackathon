import streamlit as st
import json
import os
from agent import run_assessment, generate_questions
from report import generate_pdf

st.set_page_config(page_title="SkillBridge AI", layout="wide", page_icon="🧠")

# Session State
if "jd" not in st.session_state: st.session_state.jd = ""
if "resume" not in st.session_state: st.session_state.resume = ""
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None
if "user_answers" not in st.session_state: st.session_state.user_answers = {}
if "show_questions" not in st.session_state: st.session_state.show_questions = False

# API Check
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not configured.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    st.caption("Psychology-powered Skill Assessment Agent")
    
    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if st.button("🎯 Load HR Executive Demo (Auto)", use_container_width=True):
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

        with st.spinner("Running full assessment for demo..."):
            result = run_assessment(st.session_state.jd, st.session_state.resume, {})
            st.session_state.analysis_result = result
            
            # Pre-fill realistic sample answers for video (no typing needed)
            st.session_state.user_answers = {
                "Communication": "In my counseling sessions, I use clear, empathetic communication to help clients feel heard and understood.",
                "Conflict Resolution": "I have mediated emotional conflicts between clients and family members effectively using active listening and de-escalation techniques.",
                "Emotional Intelligence": "My clinical psychology training has strengthened my emotional intelligence. I can recognize and manage emotions in high-stress situations.",
                "Recruitment": "I have limited formal experience in recruitment but I'm eager to apply my understanding of human behavior.",
                "Employee Engagement": "I understand the importance of engagement from my counseling background where building trust is essential."
            }
        
        st.success("✅ Full Demo Loaded & Analysis Completed!")
        st.session_state.show_questions = True
        st.rerun()

# Main Title
st.title("🧠 SkillBridge AI")
st.markdown("**Conversational Skill Assessment • Gap Analysis • Personalized Learning**")

# Input Fields
col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("📄 Job Description", value=st.session_state.jd, height=200, key="jd_input")
with col2:
    resume = st.text_area("📝 Resume", value=st.session_state.resume, height=200, key="resume_input")

st.session_state.jd = jd
st.session_state.resume = resume

if st.button("🔍 Analyze JD & Resume", type="primary", use_container_width=True):
    if jd.strip() and resume.strip():
        with st.spinner("Analyzing with Organizational Psychology lens..."):
            result = run_assessment(jd, resume, {})
            st.session_state.analysis_result = result
            st.session_state.show_questions = True
            st.success("✅ Analysis Complete!")
            st.rerun()

# Results Section
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "🔍 Skill Breakdown", "❓ Interview Questions", "📚 Learning Plans"])

    with tab1:
        st.subheader("Overall Assessment")
        cols = st.columns(3)
        with cols[0]:
            st.metric("Match Score", f"{result.get('match_percentage', 0)}%")
        with cols[1]:
            st.metric("Overall Level", f"{result.get('overall_score', 0)}/5")
        with cols[2]:
            st.metric("Confidence", f"{result.get('confidence', 0)}%")
        
        st.progress(result.get('match_percentage', 0)/100)
        st.write(result.get("summary", ""))

    with tab2:
        st.subheader("Skill Gap Analysis")
        for item in result.get("detailed_results", []):
            with st.expander(f"{item.get('skill')} — Gap: {item.get('gap', 0)}"):
                st.write(f"**Feedback:** {item.get('feedback', '')}")

    with tab3:
        st.subheader("Behavioral Interview Questions (Sample Answers Pre-filled)")
        st.info("For demo video - answers are pre-filled. In real use, you can edit them.")
        
        for item in result.get("detailed_results", []):
            skill = item.get("skill", "")
            st.subheader(skill)
            st.write(generate_questions(skill))
            st.text_area("Answer", 
                        value=st.session_state.user_answers.get(skill, ""), 
                        disabled=True, height=80)

    with tab4:
        st.subheader("Personalized Learning Plans")
        for item in result.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                with st.expander(f"📖 {item.get('skill')}"):
                    st.markdown(item.get("learning_plan", "Plan not generated."))

    # Export
    st.divider()
    st.subheader("Export Report")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate PDF Report"):
            pdf_path = generate_pdf(result)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, "SkillBridge_AI_Report.pdf", mime="application/pdf")

st.caption("SkillBridge AI — Conversational Assessment Agent | Built by Arunjyoti Das")
