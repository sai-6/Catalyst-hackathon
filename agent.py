import os
import json
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

from prompts import (
    comprehensive_analysis_prompt,
    question_generation_prompt,
    evaluation_prompt,
    learning_plan_prompt
)

load_dotenv()

# ---------------- API KEY ----------------
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Set it in .env or Streamlit secrets.")

client = genai.Client(api_key=API_KEY)
MODELS = ["gemini-2.0-flash-lite", "gemini-flash-latest"]

def call_gemini(prompt):
    """Reliable Gemini call with retry and fallback"""
    for model in MODELS:
        for attempt in range(4):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                print(f"⚠️ {model} attempt {attempt+1} failed: {e}")
                time.sleep(2.5)
    return "ERROR: All models failed"

def safe_json_parse(text, fallback=None):
    if fallback is None:
        fallback = {}
    try:
        return json.loads(text.strip())
    except:
        return fallback

def analyze_jd_resume(jd_text: str, resume_text: str):
    """Main intelligent analysis - JD + Resume combined"""
    prompt = comprehensive_analysis_prompt(jd_text, resume_text)
    response_text = call_gemini(prompt)
    return safe_json_parse(response_text, {
        "skill_analysis": [],
        "overall_match_percentage": 0,
        "key_strengths": [],
        "critical_gaps": [],
        "summary": "Analysis could not be completed."
    })

def generate_questions(skill):
    return call_gemini(question_generation_prompt(skill))

def evaluate_answer(skill, answer):
    if not answer or not answer.strip():
        return 3, "No answer provided - using resume-based estimate."
    response = call_gemini(evaluation_prompt(skill, answer))
    parsed = safe_json_parse(response, {"score": 3, "reason": "Invalid response"})
    score = int(parsed.get("score", 3))
    return max(1, min(5, score)), parsed.get("reason", "")

def generate_learning_plan(skill, gap):
    return call_gemini(learning_plan_prompt(skill, gap))

def run_assessment(jd_text: str, resume_text: str, user_answers: dict):
    analysis = analyze_jd_resume(jd_text, resume_text)
    
    results = []
    weighted_total = 0
    total_weight = 0

    for item in analysis.get("skill_analysis", []):
        skill = item.get("skill", "Unknown Skill")
        required = item.get("jd_required_level", 4)
        resume_level = item.get("resume_level", 3)
        
        answer = user_answers.get(skill, "")
        score, feedback = evaluate_answer(skill, answer) if answer.strip() else (resume_level, item.get("rationale", "Based on resume analysis."))
        
        gap = max(required - score, 0)
        plan = generate_learning_plan(skill, gap) if gap > 1 else "Strong match - continue building on this strength."

        weight = required
        weighted_total += score * weight
        total_weight += weight

        results.append({
            "skill": skill,
            "jd_required": required,
            "current_level": score,
            "gap": gap,
            "feedback": feedback,
            "priority": item.get("priority", "Medium"),
            "learning_plan": plan
        })

    overall = weighted_total / total_weight if total_weight > 0 else 0
    confidence = round((overall / 5) * 100, 1)

    return {
        "analysis": analysis,
        "detailed_results": results,
        "overall_score": round(overall, 2),
        "match_percentage": analysis.get("overall_match_percentage", round(overall * 20, 1)),
        "confidence": confidence,
        "key_strengths": analysis.get("key_strengths", []),
        "critical_gaps": analysis.get("critical_gaps", []),
        "summary": analysis.get("summary", "")
    }
