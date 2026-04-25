# 🧠 SkillBridge AI

**AI-Powered Skill Assessment & Personalized Learning Agent**  
*Bridging Clinical Psychology into HR & Organizational Development*

---

## 🚀 Live Demo
**[Open SkillBridge AI](https://catalyst-hackathon-38leseklrwbr9xfnesneo6.streamlit.app/)**

> **Best Experience**: Click **"🎯 Load HR Executive Demo"** for the best demonstration.

---

## 📋 Problem Statement

A resume shows **what** a candidate claims to know.  
SkillBridge AI reveals **how well** they actually know it and provides a clear, actionable path to close the gaps.

It intelligently analyzes **Job Description + Resume**, generates behavioral questions, scores responses, and creates personalized learning plans — grounded in Organizational Psychology principles.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Streamlit UI<br>Tabbed Interface] 
    --> B[Core Agent Layer<br>Python Orchestration]

    B --> C[Intelligent Analysis Engine<br>JD + Resume Combined Analysis]
    C --> D[Gemini 2.0 Flash-Lite<br>with Fallback]

    B --> E[Evaluation Engine<br>Strict 1-5 Scoring]
    B --> F[Learning Plan Engine<br>Personalized Plans]

    E & F --> G[Gap Analysis & Weighted Scoring]

    G --> H[Structured Output Layer]
    H --> I[PDF Report + JSON Export]

    style A fill:#e3f2fd
    style D fill:#f3e5f5
Key Improvement: Instead of processing skills one-by-one, the agent performs a single deep analysis of JD + Resume using an Organizational Psychology lens for better accuracy and coherence.

💡 Key Features

✅ Combined JD + Resume intelligent analysis
✅ Organizational Psychology-informed prompts and evaluation
✅ Multi-skill gap analysis with priority (High/Medium/Low)
✅ Behavioral interview questions + re-evaluation support
✅ Weighted overall match percentage + confidence score
✅ Personalized learning plans for psychology-to-HR transition
✅ Clean tabbed professional UI
✅ Professional PDF & JSON report export
✅ Retry logic + model fallback for reliability


🎯 Demo Inputs & Expected Outputs
Demo Inputs (HR Executive Role)
Job Description:
textWe are hiring an HR Executive with strong expertise in:
- Communication and Stakeholder Management
- Conflict Resolution and Mediation
- Employee Engagement and Retention Strategies
- Recruitment and Talent Acquisition
- Emotional Intelligence and Team Dynamics
Resume:
textMA in Clinical Psychology (2025). 
1 year experience as Counselor in rehabilitation setting. 
Skilled in empathy, active listening, emotional regulation, and supporting individuals through difficult situations. 
Limited corporate HR exposure but strong foundation in human behavior and psychology.
Expected Output
Executive Summary

Overall Match: 62–75%
Overall Score: 3.1 – 3.8 / 5.0
Confidence: 65–78%

Key Strengths

Emotional Intelligence
Empathy & Active Listening
Conflict Handling (transferable from counseling)

Critical Gaps

Corporate Recruitment Processes
Employee Engagement Strategies
Stakeholder Management in business context

Skill Breakdown Example:















































SkillRequiredCurrentGapPriorityEmotional Intelligence541LowCommunication532HighConflict Resolution532HighRecruitment413HighEmployee Engagement422Medium
Learning Plans include practical resources, role-play tasks, and realistic time estimates.

📊 Scoring Logic

Skill Score: 1–5 (strict evaluation based only on provided answer)
Required Level: 1–5 (based on job importance)
Gap: max(required - score, 0)
Overall Score: Weighted average = Σ(score × required) / Σ(required)
Match Percentage: Overall performance indicator
Confidence: (overall_score / 5) × 100


⚙️ Local Setup
Bashgit clone https://github.com/sai-6/Catalyst-hackathon.git
cd Catalyst-hackathon

pip install -r requirements.txt

cp .env.example .env
# Add your GOOGLE_API_KEY in .env

streamlit run app.py

🧠 About the Author
Arunjyoti Das

MA Clinical Psychology (2025)
BA Psychology (2020)
1 year experience as Counselor in rehabilitation setting

This project represents my transition from clinical psychology into AI-enabled Organizational Psychology and HR technology. SkillBridge AI applies deep understanding of human behavior and psychological assessment to create practical talent development tools.

🚀 Future Enhancements

PDF Resume/JD file upload support
Skill radar chart visualization
Adaptive multi-turn interview simulation
Candidate comparison dashboard
ATS integration


📄 Tech Stack

Frontend: Streamlit
AI: Google Gemini (gemini-2.0-flash-lite + fallback)
Backend: Python
PDF: ReportLab


Built for Deccan AI Catalyst Hackathon
Turning psychological insight into practical AI solutions for HR.

Made with ❤️ by Arunjyoti Das