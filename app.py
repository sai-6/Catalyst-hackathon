import streamlit as st
from agent import run_assessment, generate_questions, get_readme_demo_results, evaluate_candidate_answer
from report import generate_pdf
import os

st.set_page_config(page_title="SkillBridge AI", layout="wide", page_icon="🧠")

# --- SESSION STATE ---
if "jd_input" not in st.session_state: st.session_state.jd_input = ""
if "resume_input" not in st.session_state: st.session_state.resume_input = ""
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None
if "is_demo" not in st.session_state: st.session_state.is_demo = False

# --- SIDEBAR ---
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if st.button("🎯 Load HR Executive Demo", use_container_width=True):
        st.session_state.jd_input = "HR Executive: Stakeholder Management, Conflict Resolution, Recruitment."
        st.session_state.resume_input = "MA Clinical Psychology. Experience in Counseling and Mediation."
        st.session_state.is_demo = True
        st.session_state.analysis_result = get_readme_demo_results()
        st.rerun()

st.title("🧠 SkillBridge AI")
col1, col2 = st.columns(2)
with col1:
    jd_box = st.text_area("📄 Job Description", height=150, value=st.session_state.jd_input)
with col2:
    resume_box = st.text_area("📝 Resume", height=150, value=st.session_state.resume_input)

st.session_state.jd_input, st.session_state.resume_input = jd_box, resume_box

if st.button("🔍 Analyze Real-Time (API)", type="primary", use_container_width=True):
    st.session_state.is_demo = False
    with st.spinner("🧠 Running Organizational Psychology Engine..."):
        st.session_state.analysis_result = run_assessment(jd_box, resume_box)
        st.rerun()

# --- RESULTS ---
if st.session_state.analysis_result:
    res = st.session_state.analysis_result
    st.divider()
    
    col_score, col_pdf = st.columns([3, 1])
    with col_score:
        st.subheader(f"Match: {res.get('match_percentage')}%")
    with col_pdf:
        # PURELY MANUAL PDF TRIGGER
        if st.button("📄 Generate Report PDF", use_container_width=True):
            pdf_name = "SkillBridge_Report.pdf"
            generate_pdf(res, pdf_name)
            with open(pdf_name, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name=pdf_name, use_container_width=True)

    tabs = st.tabs(["📊 Summary", "🔍 Gaps", "📚 Learning", "❓ Interview"])
    
    with tabs[0]: st.write(res.get("summary"))
    with tabs[1]:
        for item in res.get("detailed_results", []):
            with st.expander(f"{item.get('skill')} (Gap: {item.get('gap')})"):
                st.write(item.get("feedback"))
    with tabs[2]:
        for item in res.get("detailed_results", []):
            st.markdown(f"### {item.get('skill')}\n{item.get('learning_plan')}")

    with tabs[3]:
        st.info("🧠 Interview Prep & Scoring")
        for item in res.get("detailed_results", []):
            skill = item.get('skill')
            q = item.get('demo_question') if st.session_state.is_demo else generate_questions(skill)
            ans_val = item.get('demo_answer') if st.session_state.is_demo else ""
            
            st.subheader(skill)
            st.write(f"**Question:** {q}")
            u_ans = st.text_area("Candidate Answer:", value=ans_val, key=f"t_{skill}")
            
            if st.button(f"Evaluate {skill}", key=f"b_{skill}"):
                if st.session_state.is_demo:
                    st.success(f"**Score: {item.get('demo_score')}/5**")
                    st.write(f"**Feedback:** {item.get('demo_reason')}")
                else:
                    with st.spinner("Scoring..."):
                        eval_res = evaluate_candidate_answer(skill, u_ans)
                        st.success(f"**Score: {eval_res.get('score')}/5**")
                        st.write(eval_res.get('reason'))
