def comprehensive_analysis_prompt(jd: str, resume: str) -> str:
    """Main powerful prompt - Analyzes JD + Resume together with Organizational Psychology lens"""
    return f"""
You are an expert **Organizational Psychologist** and Senior HR Talent Analyst with 15+ years of experience in psychological assessment and talent development.

**Job Description:**
{jd}

**Candidate Resume:**
{resume}

Perform a thorough, honest, and realistic skill gap analysis from an Organizational Psychology perspective.

### Tasks:
1. Identify all relevant skills required by the JD and demonstrated in the resume.
2. For each key skill, provide:
   - **JD Required Level** (1-5): How critical this skill is for success in the role.
   - **Resume Demonstrated Level** (0-5): How strongly the candidate shows evidence of this skill.
   - **Match Score** (0-5)
   - **Gap Description**: Clear explanation of the gap.
   - **Priority**: High, Medium, or Low
   - **Rationale**: Short explanation, especially noting transferability of clinical psychology/counseling skills to corporate HR contexts.

3. Provide:
   - **Overall Match Percentage** (realistic 0-100)
   - **Key Strengths** (list 3-5, highlight transferable soft skills like EI, empathy, etc.)
   - **Critical Gaps** (list the most important ones)
   - **Summary**: One well-written paragraph summarizing the candidate's fit and development needs.

Be constructive, specific, and realistic. Psychology graduates often excel in empathy and emotional intelligence but may lack corporate HR processes — reflect this fairly.

Return **ONLY** valid JSON. No additional text.
"""

def question_generation_prompt(skill: str) -> str:
    """Generates high-quality behavioral questions"""
    return f"""
As an Organizational Psychologist, generate **3 strong behavioral interview questions** for assessing the skill: **{skill}**.

Focus on:
- Real workplace scenarios
- Past behavior (STAR method friendly)
- Transferability from counseling/psychology background where relevant
- Emotional intelligence and self-awareness

Return only the 3 numbered questions. No extra explanation.
"""

def evaluation_prompt(skill: str, answer: str) -> str:
    """Strict evaluator with psychology background"""
    return f"""
You are a strict but fair evaluator with background in Clinical and Organizational Psychology.

Skill being assessed: **{skill}**

Candidate's Answer:
{answer}

Evaluate **only** what is written. Do not assume missing information.

**Scoring Rubric (1-5):**
1 = No meaningful understanding or irrelevant
2 = Basic awareness, very vague or generic
3 = Moderate understanding, some ideas but lacks depth/examples
4 = Strong understanding with clear relevant examples or reasoning
5 = Expert-level insight, excellent examples, strong self-awareness or psychological framing

Rules:
- Penalize vague or generic answers heavily.
- Give credit for concrete examples and reflection on human behavior.
- Be honest and developmental in your feedback.

Return **ONLY** this exact JSON format:
{{
  "score": <integer between 1 and 5>,
  "reason": "<short constructive explanation (1-2 sentences)>"
}}
"""

def learning_plan_prompt(skill: str, gap: int) -> str:
    """Practical learning plan tailored for psychology background"""
    return f"""
Create a concise, actionable, and encouraging **personalized learning plan** to close the gap in: **{skill}** (Current Gap Level: {gap}/5).

Target audience: A Clinical Psychology graduate transitioning into HR/Organizational roles.

Include these sections:
- **Key Focus Areas** (what specifically needs improvement)
- **Recommended Resources** (free or low-cost: Coursera, YouTube, articles, books, tools)
- **Practice Tasks** (2-3 specific, practical exercises — include reflection or behavioral practice)
- **Time Estimate** (realistic number of weeks)
- **Progress Milestones** (how to measure improvement)

Emphasize how to apply psychological knowledge (emotional intelligence, behavioral insights, empathy) in a corporate HR context.

Use clear bullet points and keep the tone supportive and practical.
"""

# Optional: Schema helper (for future structured output improvements)
def get_analysis_schema():
    return {
        "type": "object",
        "properties": {
            "skill_analysis": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill": {"type": "string"},
                        "jd_required_level": {"type": "integer", "minimum": 1, "maximum": 5},
                        "resume_level": {"type": "integer", "minimum": 0, "maximum": 5},
                        "match_score": {"type": "integer", "minimum": 0, "maximum": 5},
                        "gap_description": {"type": "string"},
                        "priority": {"type": "string", "enum": ["High", "Medium", "Low"]},
                        "rationale": {"type": "string"}
                    }
                }
            },
            "overall_match_percentage": {"type": "number"},
            "key_strengths": {"type": "array", "items": {"type": "string"}},
            "critical_gaps": {"type": "array", "items": {"type": "string"}},
            "summary": {"type": "string"}
        }
    }
