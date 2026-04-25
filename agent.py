import os
import json
import time
from dotenv import load_dotenv
from google import genai
import streamlit as st

from prompts import (
    skill_extraction_prompt,
    question_generation_prompt,
    evaluation_prompt,
    learning_plan_prompt
)

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- API KEY (SECURE) ----------------
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Set it in .env or Streamlit secrets.")

client = genai.Client(api_key=API_KEY)

MODELS = ["gemini-2.0-flash-lite", "gemini-flash-latest"]

# ---------------- GEMINI CALL ----------------
def call_gemini(prompt):
    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                print(f"{model} attempt {attempt+1} failed:", e)
                time.sleep(2)
    return "ERROR"

# ---------------- SAFE JSON ----------------
def safe_json_parse(text, fallback):
    try:
        return json.loads(text)
    except:
        return fallback

# ---------------- SKILL EXTRACTION ----------------
def extract_skills(jd):
    response = call_gemini(skill_extraction_prompt(jd))
    skills = safe_json_parse(response, [])
    return skills if isinstance(skills, list) else []

# ---------------- QUESTIONS ----------------
def generate_questions(skill):
    return call_gemini(question_generation_prompt(skill))

# ---------------- EVALUATION ----------------
def evaluate_answer(skill, answer):
    response = call_gemini(evaluation_prompt(skill, answer))
    parsed = safe_json_parse(response, {"score": 1, "reason": "Invalid response"})
    return int(parsed.get("score", 1)), parsed.get("reason", "")

# ---------------- GAP ----------------
def compute_gap(score, required):
    return max(required - score, 0)

# ---------------- REQUIRED LEVEL ----------------
def get_required_level(skill):
    high = ["Conflict Resolution", "Communication", "Recruitment"]
    medium = ["Employee Engagement", "Emotional Intelligence"]

    if skill in high:
        return 5
    elif skill in medium:
        return 4
    return 3

# ---------------- LEARNING PLAN ----------------
def generate_learning_plan(skill, gap):
    return call_gemini(learning_plan_prompt(skill, gap))

# ---------------- PIPELINE ----------------
def run_assessment(jd, resume, answers):
    skills = extract_skills(jd)

    results = []
    weighted_total = 0
    total_weight = 0

    for skill in skills:
        score, feedback = evaluate_answer(skill, answers.get(skill, ""))

        required = get_required_level(skill)
        gap = compute_gap(score, required)
        plan = generate_learning_plan(skill, gap)

        weight = required
        weighted_total += score * weight
        total_weight += weight

        results.append({
            "skill": skill,
            "score": score,
            "required": required,
            "gap": gap,
            "feedback": feedback,
            "learning_plan": plan
        })

    overall = weighted_total / total_weight if total_weight else 0
    confidence = round((overall / 5) * 100, 2)

    return {
        "skills": results,
        "overall_score": round(overall, 2),
        "confidence": confidence
    }
