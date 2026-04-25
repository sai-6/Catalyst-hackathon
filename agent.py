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

# --- 1. CONFIGURATION ---
# Define the list of models at the top to prevent NameError
MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]

# --- 2. API KEY & CLIENT INITIALIZATION ---
API_KEY = None
client = None

try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        API_KEY = os.getenv("GOOGLE_API_KEY")
except Exception:
    # If st.secrets isn't found at all (local use), fall back to .env
    API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the client globally for this file
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Failed to initialize Gemini Client: {e}")
else:
    client = None

# --- 3. CORE FUNCTIONS ---

def call_gemini(prompt):
    if not client:
        return "ERROR: API Key not configured in Streamlit Secrets."
        
    # Uses the MODELS list defined above
    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                # Logs specific error to Streamlit Cloud console
                print(f"Cloud Error: {model} - {str(e)}")
                time.sleep(2)
    return "ERROR: All models failed. Check Cloud Logs for details."

def safe_json_parse(text, fallback=None):
    """Cleaned up logic to handle LLM JSON outputs properly"""
    if fallback is None: fallback = {}
    if not text or "ERROR" in text: return fallback
    
    try:
        # Step 1: Attempt to find JSON block within common LLM markers
        clean_text = text.strip()
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0]
        elif "```" in clean_text:
            clean_text = clean_text.split("```")[1].split("```")[0]
            
        # Step 2: Handle cases where the LLM might have text around the JSON
        start = clean_text.find('{')
        end = clean_text.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = clean_text[start:end]
            return json.loads(json_str)
            
        return json.loads(clean_text.strip())
    except Exception as e:
        print(f"JSON Parse Error: {e}")
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
    """Safety net for demo skills and AI fallback"""
    demo_fallback = {
        "Emotional Intelligence": "How do you manage emotions in high-pressure HR situations?",
        "Conflict Resolution": "Describe a time you mediated a dispute between stakeholders.",
        "Communication": "How do you explain complex psychological insights to business leaders?",
        "Recruitment": "How do you assess cultural fit during a behavioral interview?",
        "Employee Engagement": "What strategies improve team morale in a high-stress environment?"
    }
    
    if skill in demo_fallback:
        return demo_fallback[skill]
    
    result = call_gemini(question_generation_prompt(skill))
    
    if "ERROR" in result:
        return f"Could you describe a specific situation where you demonstrated your proficiency in {skill}?"
        
    return result

def evaluate_answer(skill, answer):
    """Evaluates user answers with scoring logic"""
    if not answer or not answer.strip():
        return 3, "No answer provided - using resume-based estimate."
    
    response = call_gemini(evaluation_prompt(skill, answer))
    parsed = safe_json_parse(response, {"score": 3, "reason": "Evaluation completed based on available data."})
    
    try:
        score = int(parsed.get("score", 3))
    except:
        score = 3
    return max(1, min(5, score)), parsed.get("reason", "")

def generate_learning_plan(skill, gap):
    """Generates personalized learning steps"""
    result = call_gemini(learning_plan_prompt(skill, gap))
    if "ERROR" in result:
        return f"1. Review industry standards for {skill}.\n2. Seek mentorship in this area.\n3. Complete relevant online certifications."
    return result

def run_assessment(jd_text: str, resume_text: str, user_answers: dict):
    """Orchestrates the full assessment flow"""
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
        plan = generate_learning_plan(skill, gap) if gap > 0 else "Strong match - continue building on this strength."

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
