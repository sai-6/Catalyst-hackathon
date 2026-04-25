import os
import json
import streamlit as st
from google import genai
from prompts import (
    comprehensive_analysis_prompt, 
    learning_plan_prompt, 
    question_generation_prompt, 
    evaluation_prompt
)

# Security: Pull API Key from Streamlit Secrets
# This ensures your key is never hardcoded in the script
API_KEY = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def get_readme_demo_results():
    """
    Returns the deterministic demo results from the README file.
    This allows the app to function perfectly even if the API quota is exhausted.
    """
    return {
        "match_percentage": 68,
        "summary": "Strong psychological foundation with excellent emotional intelligence. Needs corporate HR exposure in recruitment and stakeholder management.",
        "key_strengths": ["Emotional Intelligence", "Empathy", "Conflict Resolution", "Active Listening"],
        "detailed_results": [
            {
                "skill": "Emotional Intelligence", 
                "jd_required": 5, 
                "current_level": 4, 
                "gap": 1, 
                "priority": "Low", 
                "feedback": "High clinical empathy transferable to team dynamics.", 
                "learning_plan": "Focus on applying Emotional Intelligence to corporate leadership and team mediation rather than clinical counseling."
            },
            {
                "skill": "Communication", 
                "jd_required": 5, 
                "current_level": 3, 
                "gap": 2, 
                "priority": "High", 
                "feedback": "Counseling communication is strong; needs to pivot toward corporate stakeholder management and professional presentation.", 
                "learning_plan": "Practice corporate presentation styles and business writing through LinkedIn Learning courses."
            },
            {
                "skill": "Conflict Resolution", 
                "jd_required": 5, 
                "current_level": 3, 
                "gap": 2, 
                "priority": "High", 
                "feedback": "Clinical mediation background is a strong start, but requires adaptation to workplace grievance handling.", 
                "learning_plan": "Harvard Online: 'Negotiation Mastery' and practice role-play corporate mediation exercises."
            },
            {
                "skill": "Employee Engagement", 
                "jd_required": 4, 
                "current_level": 2, 
                "gap": 2, 
                "priority": "Medium", 
                "feedback": "Understands human motivation deeply but lacks experience with corporate retention models and engagement surveys.", 
                "learning_plan": "Study corporate retention models and the implementation of Gallup Q12 surveys."
            },
            {
                "skill": "Recruitment", 
                "jd_required": 4, 
                "current_level": 1, 
                "gap": 3, 
                "priority": "High", 
                "feedback": "Limited exposure to ATS (Applicant Tracking Systems) or corporate hiring pipelines.", 
                "learning_plan": "Obtain LinkedIn Recruiter certification and undergo training on popular ATS platforms like Workday or Greenhouse."
            }
        ]
    }

def run_assessment(jd, resume):
    """
    The Live Analysis Engine using Gemini 2.0 Flash.
    Connects to the Organizational Psychologist persona in prompts.py.
    """
    if not client: 
        return {"summary": "API Key Missing. Please check Streamlit Secrets.", "detailed_results": []}
    
    prompt = comprehensive_analysis_prompt(jd, resume)
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text
        # Safety JSON parsing to handle potential conversational chatter from LLM
        data = json.loads(text[text.find('{'):text.rfind('}')+1])
        
        results = []
        for s in data.get("skill_analysis", []):
            # Calculate the Weighted Gap (Required Level - Demonstrated Level)
            req = s.get("jd_required_level", 0)
            curr = s.get("resume_demonstrated_level", 0)
            gap_val = req - curr
            
            # Generate a personalized learning plan using the learning_plan_prompt
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
        return {"summary": f"Analysis failed: {str(e)}", "detailed_results": []}

def generate_questions(skill):
    """
    Calls the question_generation_prompt to create natural, conversational
    behavioral interview questions.
    """
    if not client:
        return "As a clinical psychology graduate, how do you see your empathy helping in this role?"
        
    prompt = question_generation_prompt(skill)
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except:
        return f"Can you describe a situation where you applied psychological insights to handle {skill}?"

def evaluate_candidate_answer(skill, answer):
    """
    The Interactive Scoring Engine.
    Evaluates the user's text input against the psychology-style scoring rubric (1-5).
    """
    if not client:
        return {"score": 0, "reason": "API Key Missing. Evaluation unavailable."}
    
    prompt = evaluation_prompt(skill, answer)
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text
        # Extract and parse JSON response
        return json.loads(text[text.find('{'):text.rfind('}')+1])
    except Exception:
        return {
            "score": 0, 
            "reason": "The evaluation engine is currently unavailable. Please try again later."
        }
