import os
import json
import streamlit as st
from google import genai
from prompts import comprehensive_analysis_prompt, learning_plan_prompt

# API Config using Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def run_assessment(jd, resume):
    """Core Agent Layer using Organizational Psychologist Persona from prompts.py"""
    if not client:
        return {"summary": "API Key Missing", "detailed_results": []}

    # Restoring YOUR exact prompt function
    prompt = comprehensive_analysis_prompt(jd, resume)

    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text
        # Safety JSON parsing
        start = text.find('{')
        end = text.rfind('}') + 1
        data = json.loads(text[start:end])

        results = []
        for s in data.get("skill_analysis", []):
            gap_val = s.get("jd_required_level", 0) - s.get("resume_demonstrated_level", 0)
            
            # Using YOUR learning plan engine from prompts.py
            plan = learning_plan_prompt(s.get("skill"), gap_val)
            
            results.append({
                "skill": s.get("skill"),
                "jd_required": s.get("jd_required_level"),
                "current_level": s.get("resume_demonstrated_level"),
                "gap": gap_val,
                "priority": s.get("priority", "Medium"),
                "feedback": s.get("rationale"),
                "learning_plan": plan
            })

        return {
            "match_percentage": data.get("match_percentage", 0),
            "summary": data.get("summary", ""),
            "key_strengths": data.get("key_strengths", []),
            "detailed_results": results
        }
    except Exception as e:
        st.error(f"AI Engine Error: {e}")
        return {"detailed_results": []}

def generate_questions(skill):
    """Generates Interviewer Questions based on your architecture"""
    return f"Based on your psychological training, how would you approach a challenge involving {skill} in a corporate environment?"
