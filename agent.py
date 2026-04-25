import os, json, streamlit as st
from google import genai
from prompts import comprehensive_analysis_prompt, learning_plan_prompt

# Security: Pull API Key from Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def get_readme_demo_results():
    """Returns the deterministic demo results from the README file"""
    return {
        "match_percentage": 68,
        "summary": "Strong psychological foundation with excellent emotional intelligence. Needs corporate HR exposure in recruitment and stakeholder management.",
        "key_strengths": ["Emotional Intelligence", "Empathy", "Conflict Resolution", "Active Listening"],
        "detailed_results": [
            {"skill": "Emotional Intelligence", "jd_required": 5, "current_level": 4, "gap": 1, "priority": "Low", "feedback": "High clinical empathy transferable to team dynamics.", "learning_plan": "Apply EI to corporate leadership."},
            {"skill": "Communication", "jd_required": 5, "current_level": 3, "gap": 2, "priority": "High", "feedback": "Counseling communication is strong; needs stakeholder management focus.", "learning_plan": "Practice corporate presentation styles."},
            {"skill": "Conflict Resolution", "jd_required": 5, "current_level": 3, "gap": 2, "priority": "High", "feedback": "Clinical mediation background is a strong start.", "learning_plan": "Harvard online: 'Negotiation Mastery'."},
            {"skill": "Employee Engagement", "jd_required": 4, "current_level": 2, "gap": 2, "priority": "Medium", "feedback": "Understands human motivation but lacks corporate strategy.", "learning_plan": "Study corporate retention models."},
            {"skill": "Recruitment", "jd_required": 4, "current_level": 1, "gap": 3, "priority": "High", "feedback": "Limited exposure to ATS or corporate pipelines.", "learning_plan": "LinkedIn Recruiter certification, ATS training."}
        ]
    }

def run_assessment(jd, resume):
    """The Live Analysis Engine using Gemini API"""
    if not client: return {"summary": "API Key Missing", "detailed_results": []}
    
    prompt = comprehensive_analysis_prompt(jd, resume)
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text
        data = json.loads(text[text.find('{'):text.rfind('}')+1])
        
        results = []
        for s in data.get("skill_analysis", []):
            gap = s.get("jd_required_level", 0) - s.get("resume_demonstrated_level", 0)
            results.append({
                "skill": s.get("skill"),
                "jd_required": s.get("jd_required_level"),
                "current_level": s.get("resume_demonstrated_level"),
                "gap": gap,
                "priority": s.get("priority"),
                "feedback": s.get("rationale"),
                "learning_plan": learning_plan_prompt(s.get("skill"), gap)
            })
        return {
            "match_percentage": data.get("match_percentage", 0),
            "summary": data.get("summary", ""),
            "key_strengths": data.get("key_strengths", []),
            "detailed_results": results
        }
    except Exception as e:
        return {"summary": f"Analysis failed: {e}", "detailed_results": []}

def generate_questions(skill):
    return f"Tell me about a time you applied your clinical skills to a situation involving {skill}?"
