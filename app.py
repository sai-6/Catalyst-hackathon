import streamlit as st
import os
import time
from agent import run_assessment, generate_questions

st.set_page_config(page_title="SkillBridge AI", layout="wide", page_icon="🧠")

# --- SESSION STATE ---
if "jd_input" not in st.session_state:
    st.session_state.jd_input = ""
if "resume_input" not in st.session_state:
    st.session_state.resume_input = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("🧠 SkillBridge AI")
    if st.button("🆕 New Assessment", use_container_width=True):
        st.session_state.jd_input = ""
        st.session_state.resume_input = ""
        st.session_state.analysis_result = None
        st.rerun()

# --- MAIN UI ---
st.title("🧠 SkillBridge AI")

col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("📄 Job Description", height=250, key="jd_field", value=st.session_state.jd_input)
with col2:
    resume = st.text_area("📝 Resume", height=250, key="resume_field", value=st.session_state.resume_input)

# Force sync state
st.session_state.jd_input = jd
st.session_state.resume_input = resume

if st.button("🔍 Analyze JD & Resume", type="primary", use_container_width=True):
    if not jd.strip() or not resume.strip():
        st.error("Please enter both JD and Resume.")
    else:
        # LOGGING CHECK: This will show up in your Cloud Logs immediately
        print(f"!!! BUTTON CLICKED: Starting assessment at {time.ctime()} !!!")
        
        with st.spinner("🧠 AI is analyzing... (This takes 5-10 seconds)"):
            try:
                # Call the agent
                result = run_assessment(jd, resume, {})
                
                if result and result.get("detailed_results"):
                    st.session_state.analysis_result = result
                    st.success("✅ Analysis Complete!")
                    st.rerun()
                else:
                    st.error("AI returned empty results. Check your API Quota in the logs.")
            except Exception as e:
                st.error(f"Critical Error: {e}")
                print(f"CRITICAL ERROR: {e}")

# --- RESULTS DISPLAY ---
if st.session_state.analysis_result:
    res = st.session_state.analysis_result
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Skills", "📚 Learning Plan"])
    
    with tab1:
        st.metric("Match Score", f"{res.get('match_percentage', 0)}%")
        st.write(res.get("summary", ""))
        
    with tab2:
        for item in res.get("detailed_results", []):
            with st.expander(f"Skill: {item.get('skill')} (Level: {item.get('current_level')}/5)"):
                st.write(f"**Feedback:** {item.get('feedback')}")
                st.info(f"**Question:** {generate_questions(item.get('skill'))}")

    with tab3:
        for item in res.get("detailed_results", []):
            if item.get("gap", 0) > 0:
                st.subheader(f"Path to mastery: {item.get('skill')}")
                st.markdown(item.get("learning_plan"))
