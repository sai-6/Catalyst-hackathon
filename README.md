# 🧠 SkillBridge AI

**AI-Powered Skill Assessment & Personalized Learning Agent** *Bridging Clinical Psychology into HR & Organizational Development*

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
    A[Streamlit UI] --> B[Core Agent Layer]
    B --> C[Intelligent Analysis Engine]
    C --> D[Google Gemini 2.0 Flash]
    B --> E[Evaluation Engine]
    B --> F[Learning Plan Engine]
    E & F --> G[Gap Analysis + Weighted Scoring]
    G --> H[Structured Output]
    H --> I[PDF + JSON Export]

    style A fill:#e3f2fd,stroke:#1976d2
    style D fill:#f3e5f5,stroke:#7b1fa2
🎯 Full Demo: Input → Output1. Input DataJob Description (HR Executive):PlaintextWe are hiring an HR Executive with strong expertise in:
- Communication and Stakeholder Management
- Conflict Resolution and Mediation
- Employee Engagement and Retention Strategies
- Recruitment and Talent Acquisition
- Emotional Intelligence and Team Dynamics
Candidate Resume:PlaintextMA in Clinical Psychology (2025). 
1 year experience as Counselor in rehabilitation setting. 
Skilled in empathy, active listening, emotional regulation.
Limited corporate HR exposure but strong foundation in human behavior.
2. Analysis ResultsExecutive Summary:Match Percentage: 68%Summary: Strong psychological foundation with excellent emotional intelligence. Needs corporate HR exposure in recruitment and stakeholder management.SkillJD RequiredCurrent LevelGapPriorityEmotional Intelligence541LowCommunication532HighConflict Resolution532HighEmployee Engagement422MediumRecruitment413High📚 Personalized Learning PlansConflict Resolution: Harvard online: 'Negotiation Mastery', role-play corporate mediation exercises.Recruitment: LinkedIn Recruiter certification, ATS (Applicant Tracking System) training.⚙️ Local SetupClone & Install:Bashgit clone https://github.com/sai-6/Catalyst-hackathon.git
cd Catalyst-hackathon
pip install -r requirements.txt
Run the App:Bashstreamlit run app.py
🧠 About the AuthorArunjyoti Das | MA Clinical Psychology (2025).This project merges clinical insight with AI to solve modern HR challenges.