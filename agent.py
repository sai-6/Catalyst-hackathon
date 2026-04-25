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
# Define these at the very top so they are globally accessible
MODELS = ["gemini-1.5-flash", "gemini-2.0-flash"]
API_KEY = None
client = None

# --- 2. API KEY & CLIENT INITIALIZATION ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        API_KEY = os.getenv("GOOGLE_API_KEY")
except Exception:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"DEBUG: Client Initialization Error: {e}")

# --- 3. CORE AI LOGIC ---

def call_gemini(prompt):
    """Safe wrapper for API calls with model fallback and retries"""
    if not client:
        return "ERROR: API Client not initialized."
        
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
                print(f"DEBUG: AI Error ({model_name}): {e}")
                time.sleep(1)
                continue
    return "ERROR: All models failed or quota exceeded."

def safe_json_parse(text, fallback=None):
    """Extracts and parses JSON from potentially messy AI text"""
    if fallback is None: fallback = {}
    if not text or "ERROR" in text: return fallback
    
    try:
        clean_text = text.strip()
        # Remove markdown code blocks if present
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0]
        elif "```" in clean_text:
            clean_text = clean_text.split("```")[1].split("```")[0]
            
        # Locate the JSON object boundaries
        start = clean_text.find('{')
        end = clean_text.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(clean_text[start:end])
        return json.loads(clean_text)
    except Exception as e:
        print(f"DEBUG: JSON Parse Error: {e}")
        return fallback

# --- 4. ASSESSMENT WORKFLOW ---

def analyze_jd_resume(jd_text: str, resume_text: str):
    """Performs the initial JD-Resume match analysis"""
    prompt = comprehensive_analysis_prompt(jd_text, resume_text)
    response_text = call_gemini(prompt)
    
    # Debug the raw response in your Streamlit Logs
    print(f"DEBUG: Raw AI Response: {response_text[:100]}...") 
    
    return safe_json_parse(response_text, {
        "skill_analysis": [],
        "overall_match_percentage": 0,
        "key_strengths": [],
        "critical_gaps": [],
        "summary": "Analysis could not be completed."
    })

def generate_questions(skill):
    """Generates a technical question for a specific skill with safety fallbacks"""
    demo_fallback = {
        "Emotional Intelligence": "How do you manage emotions in high-pressure HR situations?",
        "Conflict Resolution": "Describe a time you mediated a dispute between stakeholders.",
        "Communication": "How do you explain complex psychological insights to business leaders?"
    }
    
    if skill in demo_fallback:
        return demo_fallback[skill]
    
    result = call_gemini(question_generation_prompt(skill))
    if "ERROR" in result:
        return f"Describe a specific situation where you demonstrated your proficiency in {skill}."
    return result

def evaluate_answer(skill, answer):
    """Scores the user's answer from 1-5"""
    if not answer or not answer.strip():
        return 3, "No answer provided - using resume-based estimate."
    
    response = call_gemini(evaluation_prompt(skill, answer))
    parsed = safe_json_parse(response, {"score": 3, "reason": "Evaluated based on content provided."})
    
    try:
        score = int(parsed.get("score", 3))
    except:
        score = 3
    return max(1, min(5, score)), parsed.get("reason", "")

def generate_learning_plan(skill, gap):
    """Creates a learning plan for skill gaps"""
    result = call_gemini(learning_plan_prompt(skill, gap))
    if "ERROR" in result:
        return f"1. Research {skill} industry standards.\n2. Practice real-world applications.\n3. Seek formal certification."
    return result

def run_assessment(jd_text: str, resume_text: str, user_answers: dict):
    """The main orchestration function called by app.py"""
    print("DEBUG: Starting run_assessment...") # Checkpoint 1
    
    analysis = analyze_jd_resume(jd_text, resume_text)
    print(f"DEBUG: Analysis object keys: {list(analysis.keys())}") # Checkpoint 2
    
    results = []
    weighted_total = 0
    total_weight = 0

    skill_items = analysis.get("skill_analysis", [])
    print(f"DEBUG: Found {len(skill_items)} skills to analyze.") # Checkpoint 3

    for item in skill_items:
        skill = item.get("skill", "Unknown")
        required = item.get("jd_required_level", 4)
        resume_level = item.get("resume_level", 3)
        
        answer = user_answers.get(skill, "")
        if answer and answer.strip():
            score, feedback = evaluate_answer(skill, answer)
        else:
            score, feedback = resume_level, item.get("rationale", "Resume-based estimate.")
        
        gap = max(required - score, 0)
        plan = generate_learning_plan(skill, gap) if gap > 0 else "Strong match identified."

        weighted_total += score * required
        total_weight += required

        results.append({
            "skill": skill, 
            "jd_required": required, 
            "current_level": score,
            "gap": gap, 
            "feedback": feedback, 
            "learning_plan": plan
        })

    overall = weighted_total / total_weight if total_weight > 0 else 0
    match_pct = analysis.get("overall_match_percentage", round(overall * 20, 1))
    
    print(f"DEBUG: Final Match Calculated: {match_pct}%") # Checkpoint 4

    return {
        "analysis": analysis,
        "detailed_results": results,
        "overall_score": round(overall, 2),
        "match_percentage": match_pct,
        "summary": analysis.get("summary", "")
    }
