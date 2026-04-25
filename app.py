import streamlit as st
from agent import run_assessment, generate_questions, get_readme_demo_results, evaluate_candidate_answer
from report import generate_pdf

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
    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if st.button("🎯 Load HR Executive Demo", use_container_width=True):
        st.session_state.jd_input = README_JD
        st.session_state.resume_input = README_RESUME
        st.session_state.analysis_result = get_readme_demo_results()
        st.rerun()

st.title("🧠 SkillBridge AI")
col1, col2 = st.columns(2)
with col1:
    jd_box = st.text_area("📄 Job Description", height=200, value=st.session_state.jd_input)
with col2:
    resume_box = st.text_area("📝 Resume", height=200, value=st.session_state.resume_input)

st.session_state.jd_input = jd_box
st.session_state.resume_input = resume_box

if st.button("🔍 Analyze Real-Time (API)", type="primary", use_container_width=True):
    if not jd_box.strip() or not resume_box.strip():
        st.error("Please provide both inputs.")
    else:
        with st.spinner("🧠 Running Organizational Psychology Engine..."):
            st.session_state.analysis_result = run_assessment(jd_box, resume_box)
            st.rerun()

# --- RESULTS ENGINE ---
if st.session_state.analysis_result:
    res = st.session_state.analysis_result
    st.divider()
    
    col_score, col_pdf = st.columns([3, 1])
    with col_score:
        st.subheader("📊 Executive Summary")
        st.metric("Overall Match Percentage", f"{res.get('match_percentage', 0)}%")
    
    with col_pdf:
        # OPTIONAL PDF GENERATION: Now applies to both Demo and API
        def prepare_report():
            pdf_path = "SkillBridge_AI_Report.pdf"
            generate_pdf(res, pdf_path)
            with open(pdf_path, "rb") as f: return f.read()

        st.download_button(
            label="📥 Generate & Download PDF",
            data=prepare_report(),
            file_name="SkillBridge_Assessment_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "🔍 Gap Analysis", "📚 Learning Plans", "❓ Interview Prep"])
    
    with tab1:
        st.write(res.get("summary", ""))
        
    with tab2:
        for item in res.get("detailed_results", []):
            with st.expander(f"**{item.get('skill')}** (Gap: {item.get('gap')})"):
                st.write(f"**Rationale:** {item.get('feedback')}")

    with tab3:
        for item in res.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                st.subheader(f"Strategy: {item.get('skill')}")
                st.markdown(item.get("learning_plan"))

    with tab4:
        st.info("🧠 **Real-Time Scoring:** Answer the questions below to receive an instant evaluation.")
        for item in res.get("detailed_results", []):
            skill_name = item.get('skill')
            st.subheader(f"Topic: {skill_name}")
            st.write(generate_questions(skill_name))
            
            user_ans = st.text_area(f"Your Response for {skill_name}:", key=f"ans_{skill_name}")
            if st.button(f"Evaluate {skill_name} Response", key=f"btn_{skill_name}"):
                if user_ans.strip():
                    with st.spinner("Evaluating psychology-to-HR bridge..."):
                        score_data = evaluate_candidate_answer(skill_name, user_ans)
                        st.success(f"**Score: {score_data.get('score')}/5**")
                        st.write(f"**Interviewer Feedback:** {score_data.get('reason')}")
                else:
                    st.warning("Please enter an answer to evaluate.")
