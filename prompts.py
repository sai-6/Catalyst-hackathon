def skill_extraction_prompt(jd):
    return f"""
Extract key skills from this Job Description.

Return ONLY valid JSON:
{{ "skills": ["Skill1", "Skill2"] }}

Rules:
- 5–10 skills max
- No explanation

JD:
{jd}
"""


def required_level_prompt(skill, jd):
    return f"""
Determine required level for skill: "{skill}"

Scale:
1 Basic | 2 Beginner | 3 Working | 4 Strong | 5 Critical

Return ONLY:
Level: <1-5>

JD:
{jd}
"""


def question_generation_prompt(skill):
    return f"Generate 1 clear interview question for: {skill}"


def evaluation_prompt(skill, answer):
    return f"""
Evaluate strictly.

Skill: {skill}
Answer: {answer}

Rules:
- Do NOT assume missing info
- Be strict

Return:
Score: <1-5>
Reason: short
"""


def followup_question_prompt(skill, question, answer):
    return f"""
Skill: {skill}
Question: {question}
Answer: {answer}

Ask 1 deep follow-up question.
"""


def adaptive_question_prompt(skill, score):
    return f"""
Skill: {skill}
Score: {score}

Generate next question:
- 4–5 → advanced
- 2–3 → conceptual
- 1 → basic
"""


def learning_plan_prompt(skill, gap):
    return f"""
Create learning plan for {skill}

Gap: {gap}

Include:
- Adjacent skills
- Time estimate
- Resources
- Tasks
"""
