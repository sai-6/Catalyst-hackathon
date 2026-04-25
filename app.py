import streamlit as st
import os
from agent import *

st.set_page_config(page_title="SkillBridge AI", layout="centered")

# 🔐 API CHECK
if not os.getenv("GOOGLE_API_KEY") and "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing API Key. Add in .env or Streamlit secrets.")
    st.stop()

# UI
st.title("🧠 SkillBridge AI Interview")

if "skills" not in st.session_state:
    st.session_state.skills = []

if "index" not in st.session_state:
    st.session_state.index = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "question" not in st.session_state:
    st.session_state.question = ""

jd = st.text_area("Paste Job Description")

if st.button("Start Interview"):
    st.session_state.skills = extract_skills(jd)
    st.session_state.index = 0
    st.session_state.answers = {}
    st.session_state.question = generate_questions(st.session_state.skills[0])

if st.session_state.skills:

    skill = st.session_state.skills[st.session_state.index]

    st.subheader(f"Skill: {skill}")
    st.progress((st.session_state.index+1)/len(st.session_state.skills))

    st.write(st.session_state.question)

    answer = st.text_area("Your Answer", key=f"ans_{skill}")

    if st.button("Submit Answer"):

        st.session_state.answers[skill] = answer

        score, feedback = evaluate_answer(skill, answer)

        st.write(f"Score: {score}/5")
        st.write(feedback)

        followup = generate_followup(skill, st.session_state.question, answer)
        st.session_state.question = followup

    if st.button("Next Skill"):

        st.session_state.index += 1

        if st.session_state.index < len(st.session_state.skills):
            st.session_state.question = generate_questions(
                st.session_state.skills[st.session_state.index]
            )
        else:
            result = run_assessment(jd, "", st.session_state.answers)

            st.success("Interview Complete")
            st.metric("Score", result["overall_score"])
            st.metric("Confidence", f"{result['confidence']}%")

            for r in result["skills"]:
                st.write(f"{r['skill']} → {r['score']}")
