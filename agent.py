import os, json, streamlit as st
from google import genai
from prompts import comprehensive_analysis_prompt, learning_plan_prompt

# API Config
API_KEY = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def get_demo_results():
    """Returns the hardcoded psychology assessment results (Works without API)"""
    return {
        "match_percentage": 68,
        "summary": "The candidate shows a strong psychological foundation with excellent emotional intelligence. There is a clear gap in corporate HR administrative processes, but their background in counseling makes them a high-potential mediator.",
        "key_strengths": ["Advanced Empathy", "Emotional Regulation", "Active Listening", "Behavioral Analysis"],
        "detailed_results": [
            {
                "skill": "Emotional Intelligence", "jd_required": 5, "current_level": 4, "gap": 1, "priority": "Low",
                "feedback": "Deep clinical understanding of human emotions allows for high-level team management.",
                "learning_plan": "Focus on applying EI to corporate leadership rather than clinical counseling."
            },
            {
                "skill": "Conflict Resolution", "jd_required": 5, "current_level": 3, "gap": 2, "priority": "High",
                "feedback": "Strong mediation skills in a clinical setting need to transition to corporate workplace disputes.",
                "learning_plan": "Take Harvard online: 'Negotiation Mastery' and practice role-play mediation."
            },
            {
                "skill": "Recruitment & Talent Acquisition", "jd_required": 4, "current_level": 1, "gap": 3, "priority": "High",
                "feedback": "Limited experience with ATS or corporate hiring pipelines.",
                "learning_plan": "Obtain LinkedIn Recruiter certification and learn Applicant Tracking Systems."
            }
        ]
    }

def run_assessment(jd, resume):
    """The Real-Time Engine (Uses Gemini API)"""
    if not client: return {"summary": "API Key Missing in Secrets", "detailed_results": []}
    
    prompt = comprehensive_analysis_prompt(jd, resume)
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        data = json.loads(response.text[response.text.find('{'):response.text.rfind('}')+1])
        
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
    except:
        return {"summary": "Error calling API.", "detailed_results": []}

def generate_questions(skill):
    return f"Can you describe a situation where your psychological background helped you resolve a challenge in {skill}?"
