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
    A[Streamlit UI<br>Tabbed Interface] --> B[Core Agent Layer]
    B --> C[Intelligent Analysis Engine<br>JD + Resume Combined]
    C --> D[Google Gemini 2.0 Flash]
    B --> E[Evaluation Engine<br>Strict 1-5 Scoring]
    B --> F[Learning Plan Engine]
    E & F --> G[Gap Analysis + Weighted Scoring]
    G --> H[Structured Output]
    H --> I[PDF + JSON Export]

    style A fill:#e3f2fd,stroke:#1976d2
    style D fill:#f3e5f5,stroke:#7b1fa2
🎯 Full Demo: Input → OutputInput (HR Executive Role)Job Description:PlaintextWe are hiring an HR Executive with strong expertise in:
- Communication and Stakeholder Management
- Conflict Resolution and Mediation
- Employee Engagement and Retention Strategies
- Recruitment and Talent Acquisition
- Emotional Intelligence and Team Dynamics
Resume:PlaintextMA in Clinical Psychology (2025). 
1 year experience as Counselor in rehabilitation setting. 
Skilled in empathy, active listening, emotional regulation, and supporting individuals through difficult situations. 
Limited corporate HR exposure but strong foundation in human behavior and psychology.
Expected Output (After Clicking "Load HR Executive Demo")Executive SummaryOverall Match Percentage: 68%Overall Score: 3.1 – 3.8 / 5.0Summary: Strong psychological foundation with excellent emotional intelligence and conflict resolution skills from counseling experience. Needs corporate HR exposure in recruitment and stakeholder management.Key StrengthsExceptional emotional intelligence from clinical psychology background.Proven conflict resolution skills from counseling practice.Strong empathy and active listening abilities.📊 Skill Breakdown TableSkillRequiredCurrentGapPriorityEmotional Intelligence541LowCommunication532HighConflict Resolution532HighRecruitment413HighEmployee Engagement422Medium📚 Sample Learning PlanSkill: Recruitment (Gap: 3)Focus Areas: Corporate hiring processes and ATS management.Resources: LinkedIn Recruiter Certification.Practice Tasks: ATS training and behavioral interviewing workshops.💡 Key Features✅ Intelligent Analysis: Combined JD + Resume analysis for realistic gap detection.✅ Psychology-Informed: Prompts designed by an Organizational Psychology perspective.✅ Behavioral Assessment: Generates natural, interviewer-style questions.✅ Learning Plans: Actionable steps to bridge specific skill gaps.✅ Professional Exports: Generate PDF reports for candidates or recruiters.⚙️ Local SetupClone the repository:Bashgit clone [https://github.com/sai-6/Catalyst-hackathon.git](https://github.com/sai-6/Catalyst-hackathon.git)
cd Catalyst-hackathon
Install dependencies:Bashpip install -r requirements.txt
Configure Environment:Create a .env file and add your key:PlaintextGOOGLE_API_KEY=your_api_key_here
Run the App:Bashstreamlit run app.py
🧠 About the AuthorArunjyoti Das MA Clinical Psychology (2025) | BA Psychology (2020) This project merges clinical insight with AI-enabled Organizational Psychology to solve modern HR challenges.