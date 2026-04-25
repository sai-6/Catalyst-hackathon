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

# Demo Data - Embedded directly in code
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
        {
            "skill": "Emotional Intelligence",
            "gap": 10,
            "feedback": "Excellent foundation from counseling work. Can directly apply to team dynamics and leadership.",
            "learning_plan": "1. Read 'Emotional Intelligence 2.0' by Travis Bradberry\n2. Practice EQ assessments with corporate scenarios\n3. Complete LinkedIn Learning: 'Developing Executive Presence'"
        },
        {
            "skill": "Conflict Resolution",
            "gap": 15,
            "feedback": "Strong mediation skills from family counseling. Translate to workplace scenarios.",
            "learning_plan": "1. Case studies: Workplace conflict scenarios\n2. Harvard online: 'Negotiation Mastery'\n3. Role-play corporate mediation exercises"
        },
        {
            "skill": "Communication",
            "gap": 25,
            "feedback": "Empathetic communication strong. Needs corporate stakeholder communication practice.",
            "learning_plan": "1. Toastmasters or corporate communication workshop\n2. Practice executive presentations\n3. LinkedIn Learning: 'Strategic Communication'"
        },
        {
            "skill": "Employee Engagement",
            "gap": 45,
            "feedback": "Psychology knowledge applicable but lacks corporate retention strategy experience.",
            "learning_plan": "1. Gallup employee engagement courses\n2. Study retention benchmarking data\n3. Analyze company turnover case studies"
        },
        {
            "skill": "Recruitment",
            "gap": 60,
            "feedback": "No corporate recruitment experience. Strong assessment skills can be leveraged.",
            "learning_plan": "1. LinkedIn Recruiter certification\n2. ATS (Applicant Tracking System) training\n3. Behavioral interviewing workshops"
        }
    ]
}

DEMO_USER_ANSWERS = {
    "Emotional Intelligence": "I have developed strong emotional intelligence through my counseling work, helping clients regulate emotions during difficult sessions. I can read emotional cues quickly and respond appropriately, which I believe translates well to managing team dynamics.",
    "Conflict Resolution": "In counseling, I mediated emotional conflicts between family members and clients effectively. I've de-escalated high-tension situations and found win-win solutions, skills directly applicable to workplace mediation.",
    "Communication": "I communicate clearly and empathetically with clients from diverse backgrounds in therapy sessions. My active listening skills help build trust quickly, essential for stakeholder management.",
    "Employee Engagement": "While my experience is clinical, I understand motivation theories and can apply them to retention strategies. Need corporate context but have strong behavioral insights.",
    "Recruitment": "Limited experience but skilled in psychological assessment. Eager to learn corporate hiring processes and ATS systems."
}

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
        st.session_state.jd = DEMO_JD
        st.session_state.resume = DEMO_RESUME
        st.session_state.analysis_result = DEMO_ANALYSIS_RESULT
        st.session_state.user_answers = DEMO_USER_ANSWERS
        st.success("✅ Demo Loaded with Complete Analysis!")
        st.rerun()

# Main UI - FIXED INPUTS
st.title("🧠 SkillBridge AI")
st.markdown("**AI-Powered Skill Assessment • Gap Analysis • Personalized Learning Plans**")

col1, col2 = st.columns(2)
with col1:
    st.session_state.jd = st.text_area("📄 Job Description", 
                                     value=st.session_state.jd, 
                                     height=220,
                                     key="jd_input_fixed")
with col2:
    st.session_state.resume = st.text_area("📝 Resume", 
                                         value=st.session_state.resume, 
                                         height=220,
                                         key="resume_input_fixed")

if st.button("🔍 Analyze JD & Resume", type="primary", use_container_width=True):
    if not st.session_state.jd.strip() or not st.session_state.resume.strip():
        st.error("Please provide both JD and Resume.")
    else:
        with st.spinner("Analyzing..."):
            result = run_assessment(st.session_state.jd, st.session_state.resume, {})
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
