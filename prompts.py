def skill_extraction_prompt(jd):
    return f"""
Extract all key skills from this Job Description.

Return ONLY a valid JSON list.

JD:
{jd}
"""


def question_generation_prompt(skill):
    return f"""
Generate 3 practical interview questions for: {skill}.
"""


def evaluation_prompt(skill, answer):
    return f"""
You are a strict evaluator.

Evaluate ONLY what is written. Do NOT assume missing info.

Skill: {skill}

Answer:
{answer}

Scoring:
1 = No understanding
2 = Basic
3 = Moderate
4 = Strong
5 = Expert

Rules:
- Do NOT over-score vague answers
- Penalize lack of examples

Return ONLY JSON:
{{
  "score": number,
  "reason": "short explanation"
}}
"""


def learning_plan_prompt(skill, gap):
    return f"""
Create a short learning plan for {skill}.

Gap: {gap}

Include:
- Resources
- Practice tasks
- Time estimate
"""
