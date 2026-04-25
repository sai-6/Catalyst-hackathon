import streamlit as st
from agent import *
import os

st.set_page_config(page_title="SkillBridge AI", layout="wide")

# ---------------- INIT SESSION ----------------
if "jd" not in st.session_state:
    st.session_state.jd = ""

if "resume" not in st.session_state:
    st.session_state.resume = ""

if "skills" not in st.session_state:
    st.session_state.skills = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

# ---------------- SECURITY CHECK ----------------
if not os.getenv("GOOGLE_API_KEY") and "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ API key missing")
    st.stop()

# ---------------- NEW ASSESSMENT ----------------
if st.button("🆕 New Assessment"):
    st.session_state.clear()
    st.rerun()

# ---------------- DEMO MODE (IMPORTANT: BEFORE UI) ----------------
if st.button("🎯 Load Demo Scenario"):
    st.session_state.jd = """We are hiring an HR Executive with strong skills in Communication,
Conflict Resolution, Emotional Intelligence, Recruitment, and Employee Engagement."""

    st.session_state.resume = """MA Clinical Psychology graduate with 1 year experience in counseling.
Strong in empathy and emotional understanding. No corporate HR experience."""

    st.session_state.skills = [
        "Communication",
        "Conflict Resolution",
        "Emotional Intelligence",
        "Recruitment",
        "Employee Engagement"
    ]

    st.session_state.answers = {
        "Communication": "Therapy communication but no workplace emails",
        "Conflict Resolution": "Handled emotional conflicts but not workplace disputes",
        "Emotional Intelligence": "Strong counseling-based understanding",
        "Recruitment": "No experience",
        "Employee Engagement": "Basic awareness"
    }

    st.success("✅ Demo loaded")
    st.rerun()

# ---------------- TITLE ----------------
st.title("🧠 SkillBridge AI")
st.subheader("AI-Powered Skill Assessment & Learning Agent")

# ---------------- INPUTS ----------------
jd = st.text_area("Job Description", key="jd")
resume = st.text_area("Resume", key="resume")

# ---------------- SKILL EXTRACTION ----------------
if st.button("Extract Skills"):
    st.session_state.skills = extract_skills(jd)

# ---------------- INTERVIEW ----------------
answers = {}

if st.session_state.skills:
    st.write("### 🧩 Extracted Skills")
    st.write(st.session_state.skills)

    for i, skill in enumerate(st.session_state.skills):
        st.subheader(skill)

        st.write(generate_questions(skill))

        answers[skill] = st.text_area(
            f"Answer for {skill}",
            value=st.session_state.answers.get(skill, ""),
            key=f"{skill}_{i}"
        )

# ---------------- RUN ----------------
if st.button("Run Assessment"):
    result = run_assessment(jd, resume, answers)

    st.write("## 📊 Results")

    st.write(f"### Overall Score: {result['overall_score']}")
    st.write(f"### Confidence: {result['confidence']}%")

    if result["overall_score"] >= 4:
        st.success("✅ Strong Fit")
    elif result["overall_score"] >= 3:
        st.warning("⚠️ Trainable")
    else:
        st.error("❌ Not Ready")

    for r in result["skills"]:
        st.markdown(f"### {r['skill']}")
        st.write(f"Score: {r['score']} | Required: {r['required']} | Gap: {r['gap']}")
        st.write(r["feedback"])

        with st.expander("📘 Learning Plan"):
            st.write(r["learning_plan"])
