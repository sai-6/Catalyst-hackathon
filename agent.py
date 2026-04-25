import os
import json
import time
import streamlit as st
from google import genai

# GLOBAL CONFIG
MODELS = ["gemini-1.5-flash", "gemini-2.0-flash"]
client = None

# Initialize Client
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"LOG: Client Init Failed: {e}")

def call_gemini(prompt):
    if not client:
        return "ERROR: No Client"
    for model in MODELS:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            if response.text: return response.text
        except Exception as e:
            print(f"LOG: Model {model} failed: {e}")
            continue
    return "ERROR"

def safe_json_parse(text, fallback):
    if not text or "ERROR" in text: return fallback
    try:
        # Extract JSON between curly braces
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])
    except:
        return fallback

def run_assessment(jd, resume, answers):
    print("LOG: run_assessment triggered in agent.py")
    
    # Simple prompt for testing
    prompt = f"Analyze match between JD: {jd} and Resume: {resume}. Return JSON: {{'match_percentage': 80, 'summary': 'test', 'skill_analysis': [{{'skill': 'Communication', 'jd_required_level': 5, 'resume_level': 3, 'rationale': 'test', 'priority': 'High'}}]}}"
    
    raw_response = call_gemini(prompt)
    analysis = safe_json_parse(raw_response, {"skill_analysis": []})
    
    # Process results... (simplified for stability)
    results = []
    for item in analysis.get("skill_analysis", []):
        results.append({
            "skill": item.get("skill"),
            "current_level": item.get("resume_level"),
            "gap": item.get("jd_required_level") - item.get("resume_level"),
            "feedback": item.get("rationale"),
            "learning_plan": "Review industry basics."
        })
        
    return {
        "match_percentage": analysis.get("match_percentage", 0),
        "summary": analysis.get("summary", "Analysis failed."),
        "detailed_results": results
    }

def generate_questions(skill):
    return f"How have you applied {skill} in your past roles?"
