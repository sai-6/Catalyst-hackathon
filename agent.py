import os, json, streamlit as st
from google import genai
from prompts import comprehensive_analysis_prompt, learning_plan_prompt, question_generation_prompt

API_KEY = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def run_assessment(jd, resume):
    """Core Agent Layer using Organizational Psychologist Persona"""
    if not client: return {"summary": "API Key Missing", "detailed_results": []}

    prompt = comprehensive_analysis_prompt(jd, resume)

    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text
        data = json.loads(text[text.find('{'):text.rfind('}')+1])

        results = []
        for s in data.get("skill_analysis", []):
            # WEIGHTED GAP ENGINE
            req = s.get("jd_required_level", 0)
            curr = s.get("resume_demonstrated_level", 0)
            gap_val = req - curr
            
            # LEARNING ENGINE
            plan = learning_plan_prompt(s.get("skill"), gap_val)
            
            results.append({
                "skill": s.get("skill"),
                "jd_required": req,
                "current_level": curr,
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
    except Exception as e:
        return {"summary": "Analysis failed.", "detailed_results": []}

def generate_questions(skill):
    """Behavioral Interviewer Engine from prompts.py"""
    prompt = question_generation_prompt(skill)
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except:
        return "Can you describe how you apply psychological insights to this area?"
