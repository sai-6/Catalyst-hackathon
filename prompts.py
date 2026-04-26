def comprehensive_analysis_prompt(jd: str, resume: str) -> str:
    """Main analysis prompt - JD + Resume combined"""
    return f"""
You are an expert Organizational Psychologist and Senior HR Talent Analyst with 15+ years experience.

**Job Description:**
{jd}

**Candidate Resume:**
{resume}

Perform a deep, honest skill gap analysis from an Organizational Psychology perspective.

For each relevant skill, provide:
- JD Required Level (1-5)
- Resume Demonstrated Level (0-5)
- Match Score (0-5)
- Gap Description
- Priority (High / Medium / Low)
- Rationale (especially transferability of counseling/psychology skills to corporate HR)

Also include:
- Overall Match Percentage (realistic 0-100)
- Key Strengths (3-5 points, highlight soft skills like EI and empathy)
- Critical Gaps
- One-paragraph summary

Be realistic and constructive. Psychology graduates often excel in empathy and emotional intelligence but may lack corporate HR processes.

Return **ONLY** valid JSON. No extra text.
{{
  "match_percentage": 0-100,
  "overall_score": 0-5.0,
  "confidence": 0-100,
  "summary": "text",
  "key_strengths": ["...", "..."],
  "skill_analysis": [ {"skill": "...", "jd_required_level": 5, ...} ]
}}
"""


def question_generation_prompt(skill: str) -> str:
    """Conversational, natural interviewer-style questions"""
    return f"""
You are an experienced, warm, and professional HR interviewer conducting a behavioral interview.

Generate **3 natural and conversational behavioral questions** to assess the candidate's proficiency in: **{skill}**.

Make the questions sound like a real human interviewer would ask — friendly, engaging, and open-ended. 
Use natural language, not robotic or overly formal.

Focus on:
- Past real-life experiences
- Transferable skills from psychology or counseling background where relevant
- Self-awareness and behavioral examples

Return **only** the 3 numbered questions. Do not add any extra text or explanations.

Example tone:
"Tell me about a time when..."
"Can you walk me through how you handled..."
"How have you used your skills in ...?"
"""


def evaluation_prompt(skill: str, answer: str) -> str:
    """Strict but fair evaluator"""
    return f"""
You are a strict but fair evaluator with background in Clinical and Organizational Psychology.

Skill being assessed: **{skill}**

Candidate's Answer:
{answer}

Evaluate **only** what is written. Do not assume missing information.

Scoring Rubric (1-5):
1 = No meaningful understanding or irrelevant
2 = Basic awareness, very vague or generic
3 = Moderate understanding, some ideas but lacks depth/examples
4 = Strong understanding with clear relevant examples or reasoning
5 = Expert-level insight, excellent examples, strong self-awareness

Rules:
- Penalize vague or generic answers heavily.
- Give bonus for concrete examples and psychological insight.
- Be honest and developmental in feedback.

Return **ONLY** this JSON:
{{
  "score": <integer 1-5>,
  "reason": "<short constructive explanation (1-2 sentences)>"
}}
"""


def learning_plan_prompt(skill: str, gap: int) -> str:
    """Practical learning plan"""
    return f"""
Create a concise, actionable, and encouraging personalized learning plan to close the gap in: **{skill}** (Gap Level: {gap}/5).

Target audience: Clinical Psychology graduate transitioning into HR roles.

Include:
- Key Focus Areas
- Recommended Resources (free or low-cost)
- Practice Tasks (2-3 specific exercises)
- Realistic Time Estimate
- Progress Milestones

Emphasize applying psychological knowledge (emotional intelligence, behavioral insights, empathy) in corporate HR context.

Use clear bullet points and keep the tone supportive.
"""
