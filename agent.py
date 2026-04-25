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

# --- 1. GLOBAL CONFIGURATION ---
# We define these first so they are available to all functions [cite: 31]
MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]
API_KEY = None
client = None

# --- 2. API KEY & CLIENT INITIALIZATION ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        API_KEY = os.getenv("GOOGLE_API_KEY")
except Exception:
    # Fallback for local development [cite: 28]
    API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    try:
        # Initialize the Google GenAI client [cite: 30]
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Client Initialization Error: {e}")

# --- 3. CORE AI LOGIC ---

def call_gemini(prompt):
    """Loops through MODELS to handle quotas or failures [cite: 26]"""
    if not client:
        return "ERROR: API Key not configured."
        
    for model_name in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"AI Error ({model_name}): {e}")
                time.sleep(1)
                continue
    return "ERROR: All models failed or quota exceeded."

def safe_json_parse(text, fallback=None):
    """Extracts JSON from AI text responses [cite: 22, 24]"""
    if fallback is None: fallback = {}
    if not text or "ERROR" in text: return fallback
    
    try:
        # Clean up markdown code blocks if present
        clean_text = text.strip()
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0]
        elif "```" in clean_text:
            clean_text = clean_text.split("```")[1].split("```")[0]
            
        # Find the actual JSON object
        start = clean_text.find('{')
        end = clean_text.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(clean_text[start:end])
        return json.loads(clean_text)
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        return fallback

# --- 4. ASSESSMENT WORKFLOW ---

def analyze_jd_resume(jd_text: str, resume_text: str):
    """Performs the initial JD-Resume match analysis [cite: 21]"""
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
    """Generates a technical question for a specific skill"""
    demo_fallback = {
        "Emotional Intelligence": "How do you manage emotions in high-pressure HR situations?",
        "Conflict Resolution": "Describe a time you mediated a dispute between stakeholders.",
        "Communication": "How do you explain complex psychological insights to business leaders?"
    }
    
    if skill in demo_fallback:
        return demo_fallback[skill]
    
    result = call_gemini(question_generation_prompt(skill))
    if "ERROR" in result:
        return f"Describe a situation where you demonstrated your proficiency in {skill}."
    return result

def evaluate_answer(skill, answer):
    """Scores the user's answer from 1-5 [cite: 18, 19]"""
    if not answer or not answer.strip():
        return 3, "No answer provided - using resume-based estimate."
    
    response = call_gemini(evaluation_prompt(skill, answer))
    parsed = safe_json_parse(response, {"score": 3, "reason": "Evaluated based on content."})
    
    try:
        score = int(parsed.get("score", 3))
    except:
        score = 3
    return max(1, min(5, score)), parsed.get("reason", "")

def generate_learning_plan(skill, gap):
    """Creates a 3-step learning plan for skill gaps"""
    result = call_gemini(learning_plan_prompt(skill, gap))
    if "ERROR" in result:
        return f"1. Research {skill} basics.\n2. Practice real-world scenarios.\n3. Get certified."
    return result

def run_assessment(jd_text: str, resume_text: str, user_answers: dict):
    """Main function called by app.py [cite: 13, 15]"""
    analysis = analyze_jd_resume(jd_text, resume_text)
    results = []
    weighted_total = 0
    total_weight = 0

    for item in analysis.get("skill_analysis", []):
        skill = item.get("skill", "Unknown")
        required = item.get("jd_required_level", 4)
        resume_level = item.get("resume_level", 3)
        
        answer = user_answers.get(skill, "")
        if answer.strip():
            score, feedback = evaluate_answer(skill, answer)
        else:
            score, feedback = resume_level, item.get("rationale", "Resume-based estimate.")
        
        gap = max(required - score, 0)
        plan = generate_learning_plan(skill, gap) if gap > 0 else "Strength identified."

        weighted_total += score * required
        total_weight += required

        results.append({
            "skill": skill, "jd_required": required, "current_level": score,
            "gap": gap, "feedback": feedback, "learning_plan": plan
        })

    overall = weighted_total / total_weight if total_weight > 0 else 0
    return {
        "analysis": analysis,
        "detailed_results": results,
        "overall_score": round(overall, 2),
        "match_percentage": analysis.get("overall_match_percentage", round(overall * 20, 1)),
        "summary": analysis.get("summary", "")
    }
