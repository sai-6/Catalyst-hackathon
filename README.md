# 🧠 SkillBridge AI

**AI-Powered Skill Assessment & Personalized Learning Agent**  
*Bridging Clinical Psychology into HR & Organizational Development*

---

## 🚀 Live Demo
**[Open SkillBridge AI](https://catalyst-hackathon-38leseklrwbr9xfnesneo6.streamlit.app/)**

> **Recommended for Demo**: Click **"🎯 Load HR Executive Demo"** — it auto-runs the full analysis.

---

## 📋 Problem Statement

A resume shows **what** a candidate claims to know.  
SkillBridge AI reveals **how well** they actually know it and provides a clear path to close the gaps using Organizational Psychology principles.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Streamlit UI<br>Tabbed Interface] --> B[Core Agent Layer]
    B --> C[Intelligent Analysis Engine<br>JD + Resume Combined]
    C --> D[Google Gemini 2.0 Flash-Lite]
    B --> E[Evaluation Engine<br>Strict 1-5 Scoring]
    B --> F[Learning Plan Engine]
    E & F --> G[Gap Analysis + Weighted Scoring]
    G --> H[Structured Output]
    H --> I[PDF + JSON Export]

    style A fill:#e3f2fd,stroke:#1976d2
    style D fill:#f3e5f5,stroke:#7b1fa2

🎯 Full Demo: Input → Output
Input (HR Executive Role)
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
Expected Output (After Clicking "Load HR Executive Demo")
Executive Summary

Overall Match Percentage: 62–75%
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

Skill Breakdown Example















































SkillRequiredCurrentGapPriorityEmotional Intelligence541LowCommunication532HighConflict Resolution532HighRecruitment413HighEmployee Engagement422Medium
Learning Plans include practical resources (Coursera, Harvard ManageMentor, role-play exercises), time estimates, and progress milestones.

💡 Key Features

✅ Intelligent JD + Resume combined analysis
✅ Organizational Psychology-informed prompts
✅ Multi-skill gap analysis with priority levels
✅ Behavioral questions with re-evaluation
✅ Weighted overall match score + confidence
✅ Personalized learning plans
✅ Clean tabbed UI with automatic demo
✅ PDF and JSON export


📊 Scoring Logic

Skill Score: 1–5 (strict evaluation)
Overall Score: Weighted average
Match %: Overall performance indicator
Confidence: (overall_score / 5) × 100


⚙️ Local Setup
Bashgit clone https://github.com/sai-6/Catalyst-hackathon.git
cd Catalyst-hackathon

pip install -r requirements.txt

cp .env.example .env
# Add your GOOGLE_API_KEY

streamlit run app.py

🧠 About the Author
Arunjyoti Das
MA Clinical Psychology (2025) | BA Psychology (2020)
Former Counselor (Rehabilitation setting, 1 year)
This project is part of my transition from clinical psychology to AI-enabled Organizational Psychology and HR technology.

🚀 Future Enhancements

PDF Resume/JD file upload
Skill radar chart visualization
Adaptive multi-turn interview
ATS integration


📄 Tech Stack

Frontend: Streamlit
AI: Google Gemini (gemini-2.0-flash-lite)
PDF: ReportLab


Built for Deccan AI Catalyst Hackathon
Turning psychological insight into practical AI solutions for HR and talent development.
Made with ❤️ by Arunjyoti Das