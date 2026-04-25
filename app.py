import streamlit as st
from agent import run_assessment, generate_questions, get_readme_demo_results
from report import generate_pdf
import io

st.set_page_config(page_title="SkillBridge AI", layout="wide", page_icon="🧠")

# --- DATA FROM README DEMO SECTION ---
README_JD = """We are hiring an HR Executive with strong expertise in:
- Communication and Stakeholder Management
- Conflict Resolution and Mediation
- Employee Engagement and Retention Strategies
- Recruitment and Talent Acquisition
- Emotional Intelligence and Team Dynamics"""

README_RESUME = """MA in Clinical Psychology (2025). 1 year experience as Counselor. 
Skilled in empathy, active listening, and emotional regulation.
Limited corporate HR exposure but strong foundation in human behavior."""

# --- SESSION STATE ---
if "jd_input" not in st.session_state: st.session_state.jd_input = ""
if "resume_input" not in st.session_state: st.session_state.resume_input = ""
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    st.caption("Bridging Clinical Psychology into HR")
    
    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if st.button("🎯 Load HR Executive Demo", use_container_width=True):
        st.session_state.jd_input = README_JD
        st.session_state.resume_input = README_RESUME
        st.session_state.analysis_result = get_readme_demo_results()
        st.rerun()

st.title("🧠 SkillBridge AI")
st.markdown(f"**AI-Powered Skill Assessment & Personalized Learning Agent**")

col1, col2 = st.columns(2)
with col1:
    jd_box = st.text_area("📄 Job Description", height=250, value=st.session_state.jd_input)
with col2:
    resume_box = st.text_area("📝 Resume", height=250, value=st.session_state.resume_input)

st.session_state.jd_input = jd_box
st.session_state.resume_input = resume_box

if st.button("🔍 Analyze Real-Time (API)", type="primary", use_container_width=True):
    if not jd_box.strip() or not resume_box.strip():
        st.error("Please provide both inputs.")
    else:
        with st.spinner("🧠 Running Organizational Psychology Engine..."):
            result = run_assessment(jd_box, resume_box)
            st.session_state.analysis_result = result
            st.rerun()

# --- RESULTS ENGINE (WITH CHOICE-BASED DOWNLOAD) ---
if st.session_state.analysis_result:
    res = st.session_state.analysis_result
    st.divider()
    
    col_score, col_pdf = st.columns([3, 1])
    with col_score:
        st.subheader("📊 Executive Summary")
        st.metric("Overall Match Percentage", f"{res.get('match_percentage', 0)}%")
    
    with col_pdf:
        # OPTIONAL DOWNLOAD LOGIC: PDF is only generated on click
        def prepare_report():
            pdf_path = "SkillBridge_AI_Report.pdf"
            generate_pdf(res, pdf_path)
            with open(pdf_path, "rb") as f:
                return f.read()

        st.download_button(
            label="📥 Generate & Download PDF",
            data=prepare_report() if st.session_state.analysis_result else b"",
            file_name="SkillBridge_Assessment_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Gap Analysis", "📚 Learning Plans"])
    
    with tab1:
        st.write(res.get("summary", ""))
        st.subheader("Key Strengths")
        for s in res.get("key_strengths", []):
            st.success(s)
        
    with tab2:
        for item in res.get("detailed_results", []):
            with st.expander(f"**{item.get('skill')}** (Gap: {item.get('gap')})"):
                st.write(f"**JD Required:** {item.get('jd_required')} | **Current:** {item.get('current_level')}")
                st.write(f"**Priority:** {item.get('priority')}")
                st.write(f"**Feedback:** {item.get('feedback')}")
                st.info(f"**Interview Question:** {generate_questions(item.get('skill'))}")

    with tab3:
        for item in res.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                st.subheader(f"Strategy: {item.get('skill')}")
                st.markdown(item.get("learning_plan"))

st.caption("Made with ❤️ by Arunjyoti Das | MA Clinical Psychology")
