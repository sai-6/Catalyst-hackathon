import os, json, streamlit as st
from google import genai
from prompts import (
    comprehensive_analysis_prompt, 
    learning_plan_prompt, 
    question_generation_prompt, 
    evaluation_prompt
)

API_KEY = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def get_readme_demo_results():
    """Deterministic Demo Data - Exactly as per README (API-Free)"""
    return {
        "match_percentage": 68,
        "summary": "Strong psychological foundation with excellent emotional intelligence. Needs corporate HR exposure in recruitment and stakeholder management.",
        "key_strengths": ["Emotional Intelligence", "Empathy", "Conflict Resolution", "Active Listening"],
        "detailed_results": [
            {
                "skill": "Conflict Resolution", "jd_required": 5, "current_level": 3, "gap": 2, "priority": "High",
                "feedback": "Clinical mediation background is a strong start for workplace mediation.",
                "learning_plan": "Harvard Online: 'Negotiation Mastery' and role-play corporate mediation exercises.",
                "demo_question": "How do you handle workplace mediation between two senior stakeholders?",
                "demo_answer": "I would apply the 'Active Listening' and 'Emotional Regulation' techniques from my clinical training. By acknowledging the underlying emotions of both parties first, I can de-escalate the tension before moving toward a collaborative resolution.",
                "demo_score": 4,
                "demo_reason": "Excellent application of clinical de-escalation in a corporate hierarchy context."
            },
            {
                "skill": "Recruitment", "jd_required": 4, "current_level": 1, "gap": 3, "priority": "High",
                "feedback": "Limited exposure to ATS or corporate hiring pipelines.",
                "learning_plan": "LinkedIn Recruiter certification and ATS training.",
                "demo_question": "How would your psychology background improve our talent acquisition process?",
                "demo_answer": "I would move beyond resume matching to behavioral interviewing, looking for 'Trait-Environment Fit' to ensure long-term retention.",
                "demo_score": 3,
                "demo_reason": "Strong conceptual understanding, though lacks specific experience with corporate ATS tools."
            }
        ]
    }

def run_assessment(jd, resume):
    if not client: return {"summary": "API Key Missing", "detailed_results": []}
    prompt = comprehensive_analysis_prompt(jd, resume)
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        data = json.loads(response.text[response.text.find('{'):response.text.rfind('}')+1])
        results = []
        for s in data.get("skill_analysis", []):
            gap = s.get("jd_required_level", 0) - s.get("resume_demonstrated_level", 0)
            results.append({
                "skill": s.get("skill"), "jd_required": s.get("jd_required_level"),
                "current_level": s.get("resume_demonstrated_level"), "gap": gap,
                "priority": s.get("priority"), "feedback": s.get("rationale"),
                "learning_plan": learning_plan_prompt(s.get("skill"), gap)
            })
        return {"match_percentage": data.get("match_percentage", 0), "summary": data.get("summary", ""), "key_strengths": data.get("key_strengths", []), "detailed_results": results}
    except: return {"summary": "Analysis failed.", "detailed_results": []}

def generate_questions(skill):
    if not client: return "How does your background help you with this skill?"
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=question_generation_prompt(skill))
        return response.text
    except: return f"Describe your experience with {skill}."

def evaluate_candidate_answer(skill, answer):
    if not client: return {"score": 0, "reason": "API Key Missing"}
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=evaluation_prompt(skill, answer))
        return json.loads(response.text[response.text.find('{'):response.text.rfind('}')+1])
    except: return {"score": 0, "reason": "Evaluation unavailable."}
