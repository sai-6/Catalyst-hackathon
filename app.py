import streamlit as st
import json
import os
from agent import run_assessment, generate_questions
from report import generate_pdf

st.set_page_config(
    page_title="SkillBridge AI",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------
if "jd" not in st.session_state:
    st.session_state.jd = ""
if "resume" not in st.session_state:
    st.session_state.resume = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# ---------------- API KEY CHECK ----------------
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not configured. Please add it in Streamlit Secrets or .env file.")
    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    st.caption("Psychology-powered Skill Gap Analysis & Learning Agent")
    
    if st.button("🆕 New Assessment", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
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
        
        st.success("✅ Demo Loaded – Psychology to HR transition example")
        st.rerun()

# ---------------- MAIN UI ----------------
st.title("🧠 SkillBridge AI")
st.markdown("**AI-Powered Skill Assessment • Gap Analysis • Personalized Learning Plans**")

col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("📄 Job Description", value=st.session_state.jd, height=250,
                      placeholder="Paste the full Job Description here...", key="jd_input")
with col2:
    resume = st.text_area("📝 Resume / Candidate Profile", value=st.session_state.resume, height=250,
                          placeholder="Paste the candidate's resume here...", key="resume_input")

st.session_state.jd = jd
st.session_state.resume = resume

# ---------------- ANALYZE BUTTON ----------------
if st.button("🔍 Analyze JD & Resume", type="primary", use_container_width=True):
    if not jd.strip() or not resume.strip():
        st.error("⚠️ Please provide both Job Description and Resume.")
    else:
        with st.spinner("Analyzing with Organizational Psychology lens..."):
            result = run_assessment(jd, resume, {})
            st.session_state.analysis_result = result
            st.success("✅ Analysis Complete!")
            st.rerun()

# ---------------- RESULTS TABS ----------------
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Executive Summary", 
        "🔍 Skill Breakdown", 
        "❓ Behavioral Assessment", 
        "📚 Learning Plans"
    ])

    with tab1:
        st.subheader("Overall Match")
        cols = st.columns(3)
        with cols[0]:
            st.metric("Match %", f"{result.get('match_percentage', 0)}%")
        with cols[1]:
            st.metric("Score", f"{result.get('overall_score', 0)}/5")
        with cols[2]:
            st.metric("Confidence", f"{result.get('confidence', 0)}%")
        
        st.progress(result.get('match_percentage', 0) / 100)
        st.write(result.get("summary", ""))

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("✅ Key Strengths")
            for s in result.get("key_strengths", []):
                st.success(s)
        with col_b:
            st.subheader("⚠️ Critical Gaps")
            for g in result.get("critical_gaps", []):
                st.error(g)

    with tab2:
        st.subheader("Skill-by-Skill Analysis")
        for item in result.get("detailed_results", []):
            with st.expander(f"{item['skill']} — Gap: {item.get('gap', 0)}"):
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Required", item.get("jd_required", 0))
                with c2: st.metric("Current", item.get("current_level", 0))
                with c3: st.metric("Gap", item.get("gap", 0))
                st.write(f"**Feedback:** {item.get('feedback', '')}")

    with tab3:
        st.subheader("Behavioral Assessment Questions")
        updated_answers = {}
        for item in result.get("detailed_results", []):
            skill = item["skill"]
            st.subheader(skill)
            st.write(generate_questions(skill))
            ans = st.text_area(f"Your answer for {skill}", 
                             value=st.session_state.user_answers.get(skill, ""), 
                             height=100, key=f"ans_{skill}")
            updated_answers[skill] = ans
        st.session_state.user_answers = updated_answers

        if st.button("🔄 Re-run Assessment with Answers", type="primary"):
            with st.spinner("Re-evaluating..."):
                new_result = run_assessment(st.session_state.jd, st.session_state.resume, updated_answers)
                st.session_state.analysis_result = new_result
                st.success("✅ Re-evaluation done!")
                st.rerun()

    with tab4:
        st.subheader("Personalized Learning Plans")
        for item in result.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                with st.expander(f"📖 {item['skill']}"):
                    st.markdown(item.get("learning_plan", "Plan not generated."))

    # Export Section
    st.divider()
    st.subheader("📄 Export Reports")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate PDF Report"):
            pdf_path = generate_pdf(result)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, "SkillBridge_AI_Report.pdf", mime="application/pdf")
    with col2:
        json_data = json.dumps(result, indent=2)
        st.download_button("⬇️ Download JSON", json_data, "SkillBridge_AI_Report.json", mime="application/json")

else:
    st.info("👆 Fill JD and Resume, then click **Analyze JD & Resume**")

st.caption("SkillBridge AI — Built by Arunjyoti Das | MA Clinical Psychology")
