import os, json, streamlit as st
from google import genai
from prompts import comprehensive_analysis_prompt, learning_plan_prompt

# SECURE API SETUP
API_KEY = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def run_assessment(jd, resume):
    """Core Agent using Organizational Psychologist Persona and Gaps Engine"""
    if not client: return {"summary": "API Key Missing", "detailed_results": []}

    # RESTORED: Using YOUR exact prompt engine
    prompt = comprehensive_analysis_prompt(jd, resume)

    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text
        data = json.loads(text[text.find('{'):text.rfind('}')+1])

        results = []
        for s in data.get("skill_analysis", []):
            # THE GAP ENGINE LOGIC
            gap_val = s.get("jd_required_level", 0) - s.get("resume_demonstrated_level", 0)
            
            # THE LEARNING ENGINE LOGIC (From prompts.py)
            plan = learning_plan_prompt(s.get("skill"), gap_val)
            
            results.append({
                "skill": s.get("skill"),
                "jd_required": s.get("jd_required_level"),
                "current_level": s.get("resume_demonstrated_level"),
                "gap": gap_val,
                "priority": s.get("priority"),
                "feedback": s.get("rationale"),
                "learning_plan": plan
            })

        return {
            "match_percentage": data.get("match_percentage", 0),
            "summary": data.get("summary", ""),
            "key_strengths": data.get("key_strengths", []),
            "detailed_results": results
        }
    except Exception:
        return {"summary": "Analysis Error", "detailed_results": []}

def generate_questions(skill):
    """Generates behavioral questions for the assessment"""
    return f"How do you apply your clinical psychology empathy to manage {skill} in a corporate environment?"
