# 🧠 SkillBridge AI

**AI-Powered Skill Assessment & Personalized Learning Agent**  
*Bridging Clinical Psychology into HR & Organizational Development*

---

## 🚀 Live Demo
**[Open SkillBridge AI](https://catalyst-hackathon-38leseklrwbr9xfnesneo6.streamlit.app/)**

> **Best Experience**: Click **"🎯 Load HR Executive Demo"** button.

---

## 📋 Problem Statement

A resume shows **what** a candidate claims to know.  
SkillBridge AI reveals **how well** they actually know it and provides a clear, actionable path to close the gaps.

It intelligently analyzes **Job Description + Resume**, generates behavioral questions, scores responses, and creates personalized learning plans — grounded in Organizational Psychology.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Streamlit UI<br>Tabbed Interface] --> B[Core Agent Layer]
    B --> C[Intelligent Analysis Engine<br>JD + Resume Combined]
    C --> D[Google Gemini 2.0 Flash-Lite]
    B --> E[Evaluation Engine<br>1-5 Scoring]
    B --> F[Learning Plan Engine]
    E & F --> G[Gap Analysis + Weighted Score]
    G --> H[Structured Output]
    H --> I[PDF + JSON Export]

    style A fill:#e3f2fd,stroke:#1976d2
    style D fill:#f3e5f5,stroke:#7b1fa2

💡 Key Features

✅ Combined JD + Resume intelligent analysis
✅ Organizational Psychology-informed evaluation
✅ Multi-skill gap analysis with priority levels
✅ Behavioral interview questions + re-evaluation
✅ Weighted overall match percentage + confidence
✅ Personalized learning plans for career transition
✅ Clean tabbed professional UI
✅ PDF and JSON report export


🎯 Demo Inputs & Expected Outputs
Job Description (Demo):
textWe are hiring an HR Executive with strong expertise in:
- Communication and Stakeholder Management
- Conflict Resolution and Mediation
- Employee Engagement and Retention Strategies
- Recruitment and Talent Acquisition
- Emotional Intelligence and Team Dynamics
Resume (Demo):
textMA in Clinical Psychology (2025). 
1 year experience as Counselor in rehabilitation setting. 
Skilled in empathy, active listening, emotional regulation, and supporting individuals through difficult situations. 
Limited corporate HR exposure but strong foundation in human behavior and psychology.
Expected Results:

Overall Match: 62–75%
Key Strengths: Emotional Intelligence, Empathy, Conflict Handling
Critical Gaps: Recruitment processes, Corporate Employee Engagement
Learning plans with practical resources and timelines


📊 Scoring Logic

Skill Score: 1–5 (strict)
Overall Score: Weighted average
Match %: Overall performance
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
Former Counselor (1 year experience)
This project represents my transition from clinical psychology to AI-enabled Organizational Psychology and HR technology.

🚀 Future Enhancements

PDF file upload support
Skill visualization charts
Adaptive interview simulation
ATS integration


📄 Tech Stack

Frontend: Streamlit
AI: Google Gemini
PDF: ReportLab


Built for Deccan AI Catalyst Hackathon
Turning psychological insight into practical AI solutions for HR.
Made with ❤️ by Arunjyoti Das