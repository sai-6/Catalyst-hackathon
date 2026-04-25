import os, time, json, re
from dotenv import load_dotenv
from google import genai
import streamlit as st
from prompts import *

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

models = ["gemini-2.0-flash-lite", "gemini-flash-latest"]


def call_gemini(prompt):
    for model in models:
        for _ in range(2):
            try:
                res = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return res.text
            except:
                time.sleep(1)
    return "Error: Model unavailable"


def parse_skills(text):
    try:
        return json.loads(text)["skills"]
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group()).get("skills", [])
    return []


def extract_number(text):
    m = re.search(r'\b([1-5])\b', text)
    return int(m.group(1)) if m else 3


def extract_skills(jd):
    return parse_skills(call_gemini(skill_extraction_prompt(jd)))


def generate_questions(skill):
    return call_gemini(question_generation_prompt(skill))


def get_required_level(skill, jd):
    return extract_number(call_gemini(required_level_prompt(skill, jd)))


def evaluate_answer(skill, ans):
    res = call_gemini(evaluation_prompt(skill, ans))
    return extract_number(res), res


def compute_gap(score, required):
    raw = max(required - score, 0)
    weighted = raw * (required / 5)
    return round(weighted, 2), raw


def generate_followup(skill, question, answer):
    return call_gemini(followup_question_prompt(skill, question, answer))


def generate_adaptive_question(skill, score):
    return call_gemini(adaptive_question_prompt(skill, score))


def generate_learning_plan(skill, gap):
    return call_gemini(learning_plan_prompt(skill, gap))


def compute_confidence(results):
    scores = [r["score"] for r in results]
    gaps = [r["gap"] for r in results]
    avg_score = sum(scores) / len(scores)
    avg_gap = sum(gaps) / len(gaps)
    return round((avg_score/5)*(1-(avg_gap/5))*100, 2)


def run_assessment(jd, resume, answers):
    skills = extract_skills(jd)
    results = []

    for skill in skills:
        required = get_required_level(skill, jd)
        score, feedback = evaluate_answer(skill, answers.get(skill, ""))

        weighted_gap, raw_gap = compute_gap(score, required)
        plan = generate_learning_plan(skill, raw_gap)

        results.append({
            "skill": skill,
            "required": required,
            "score": score,
            "gap": weighted_gap,
            "raw_gap": raw_gap,
            "feedback": feedback,
            "learning_plan": plan
        })

    overall = round(sum(r["score"] for r in results)/len(results), 2)
    confidence = compute_confidence(results)

    return {"skills": results, "overall_score": overall, "confidence": confidence}
