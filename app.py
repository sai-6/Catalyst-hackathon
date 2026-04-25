import streamlit as st
import json
import os
import time
from agent import run_assessment, generate_questions
# from report import generate_pdf # Ensure this file exists, otherwise comment it out

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
    "summary": "Strong psychological foundation with excellent emotional intelligence and conflict resolution skills from counseling experience. Needs corporate HR exposure.",
    "key_strengths": [
        "Exceptional emotional intelligence from clinical psychology background",
        "Proven conflict resolution skills from counseling practice"
    ],
    "detailed_results": [
        {"skill": "Emotional Intelligence", "gap": 10, "feedback": "Excellent foundation.", "learning_plan": "1. Read 'Emotional Intelligence 2.0'"},
        {"skill": "Conflict Resolution", "gap": 15, "feedback": "Strong mediation skills.", "learning_plan": "1. Harvard 'Negotiation Mastery'"}
    ]
}

DEMO_USER_ANSWERS = {
    "Emotional Intelligence": "I have developed strong emotional intelligence through my counseling work...",
    "Conflict Resolution": "In counseling, I mediated emotional conflicts between family members..."
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

# --- SIDEBAR ---
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    st.caption("Psychology-powered Skill Gap Analysis")

    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.jd_input = ""
        st.session_state.resume_input = ""
        st.session_state.analysis_result = None
        st.session_state.user_answers = {}
        st.rerun()

    if st.button("🎯 Load HR Executive Demo", use_container_width=True):
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
    jd = st.text_area("📄 Job Description", height=220, key="jd_input_widget", value=st.session_state.jd_input)
with col2:
    resume = st.text_area("📝 Resume", height=220, key="resume_input_widget", value=st.session_state.resume_input)

# Update state from widget
st.session_state.jd_input = jd
st.session_state.resume_input = resume

if st.button("🔍 Analyze JD & Resume", type="primary", use_container_width=True):
    if not st.session_state.jd_input.strip() or not st.session_state.resume_input.strip():
        st.error("Please provide both JD and Resume.")
    else:
        # Check API Key before running
        API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        if not API_KEY:
            st.error("❌ API Key not found. Please configure it in Secrets.")
        else:
            with st.spinner("🧠 AI is analyzing skills and psychology..."):
                try:
                    # Trigger the function in agent.py
                    result = run_assessment(st.session_state.jd_input, st.session_state.resume_input, {})
                    st.session_state.analysis_result = result
                    st.success("✅ Analysis Complete!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

# --- SHOW RESULTS ---
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "🔍 Skill Breakdown", "❓ Assessment", "📚 Learning Plans"])

    with tab1:
        match_val = result.get('match_percentage', 0)
        st.metric("Match Percentage", f"{match_val}%")
        st.progress(min(max(match_val / 100, 0.0), 1.0))
        st.write(result.get("summary", "No summary available."))
        
        st.subheader("Key Strengths")
        strengths = result.get("key_strengths", [])
        if strengths:
            for s in strengths:
                st.success(s)
        else:
            st.write("No specific strengths identified.")

    with tab2:
        for item in result.get("detailed_results", []):
            skill_name = item.get('skill', 'Unknown Skill')
            gap_val = item.get('gap', 0)
            with st.expander(f"{skill_name} (Gap Score: {gap_val})"):
                st.write(f"**Feedback:** {item.get('feedback', 'No feedback provided.')}")

    with tab3:
        st.info("The AI has generated specific questions based on the gaps found.")
        for item in result.get("detailed_results", []):
            skill = item.get("skill", "")
            st.subheader(f"Assess: {skill}")
            # Dynamic question generation
            question = generate_questions(skill)
            st.markdown(f"> {question}")
            
            ans_val = st.session_state.user_answers.get(skill, "")
            st.text_area("Your Response", value=ans_val, height=100, key=f"ans_{skill}")

    with tab4:
        for item in result.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                with st.expander(f"📚 Roadmap: {item.get('skill', '')}"):
                    st.markdown(item.get("learning_plan", "No plan available."))

    st.divider()
    if st.button("Generate PDF Report"):
        st.info("PDF generation is being processed...")
        # Add your generate_pdf logic here if the file exists

st.caption(f"SkillBridge AI — Built by Arunjyoti Das | MA Clinical Psychology")
