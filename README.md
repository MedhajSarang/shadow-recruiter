# Shadow Recruiter AI 🤖

**Live Application:** https://shadow-recruiter.streamlit.app/  
**Backend API Documentation:** https://shadow-recruiter.onrender.com/docs  

## Overview
Shadow Recruiter AI is a multi-tenant, containerized microservice application designed to conduct data-driven technical mock interviews. 

It ingests a candidate's resume and a target job description, calculates a real-time Cosine Similarity match score, and deploys an autonomous AI agent to conduct a rigorous technical Q&A session targeting the candidate's specific missing skills.

## The Tech Stack
This project bridges the gap between Data Science and Backend Engineering, implementing a decoupled architecture deployed across dual cloud environments.

* **Frontend (User Interface):** Built with **Python & Streamlit**. Handles continuous chat state machines, dynamic user sessions, and historical data visualization. Deployed on Streamlit Community Cloud.
* **Backend (REST API):** Built with **FastAPI**. Handles routing, prompt engineering, and database connection pooling. Deployed as a Dockerized web service on Render.
* **Database (Storage):** Hosted on **Supabase (PostgreSQL)**. Utilizes a multi-tenant relational structure to track user history and performance metrics using **SQL**.
* **AI Engine:** Powered by **Google Gemini 2.5 Flash** for rapid, highly accurate resume parsing and technical candidate evaluation.

## Key Engineering Achievements
* **Secure Authentication:** Implemented a custom login gate using `passlib` and `bcrypt`. Handled the cryptographic 72-byte hashing limit at the machine-code level prior to database insertion.
* **Continuous State Machine:** Overcame Streamlit's default page-refresh amnesia by engineering a robust session state vault to support a continuous two-way chat loop without losing data.
* **Dockerized Deployment:** Both microservices are containerized via a `docker-compose.yml` network, ensuring absolute parity between local development and cloud production.
* **Cold-Start Mitigation:** Engineered a cron-job ping system to bypass container cold-start latency on free-tier cloud providers.

## Local Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/MedhajSarang/shadow-recruiter.git
cd shadow-recruiter
```
**2. Configure Environment Variables**
Create a .env file in the root directory and add your credentials. (Note: Never commit this file to version control).
```bash
GEMINI_API_KEY=your_google_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```
**3. Boot the Matrix (Docker Required)**
Ensure docker desktop is running then execute:
```bash
docker-compose up --build
```
Frontend will be available at: http://localhost:8501 Backend API docs available at: http://localhost:8000/docs
