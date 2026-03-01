from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import shutil
import os


# Import all 6 of our custom services
from backend.services.pdf_parser import extract_text_from_pdf
from backend.services.data_cleaner import clean_text
from backend.services.scraper import scrape_job_description
from backend.services.ml_engine import calculate_match_score, extract_missing_keywords
from backend.services.db_service import log_interview_session, get_interview_history
from backend.services.ai_service import generate_interview_question, evaluate_candidate_answer

class ChatPayload(BaseModel):
    question: str
    answer: str

app = FastAPI(title="Shadow Recruiter API")

@app.post("/api/analyze")
async def analyze_application(
    job_url: str = Form(...), 
    job_role: str = Form(...), 
    resume: UploadFile = File(...)
):
    try:
        # 1. Save uploaded PDF temporarily to the server
        temp_pdf_path = f"temp_{resume.filename}"
        with open(temp_pdf_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        
        # 2. Extract and Clean Resume
        raw_resume = extract_text_from_pdf(temp_pdf_path)
        clean_resume = clean_text(raw_resume)
        os.remove(temp_pdf_path) # Clean up the temp file immediately
        
        # 3. Scrape and Clean Job Description
        raw_jd = scrape_job_description(job_url)
        clean_jd = clean_text(raw_jd)
        
        # 4. Math Engine Analysis
        match_score = calculate_match_score(clean_resume, clean_jd)
        missing_skills = extract_missing_keywords(clean_resume, clean_jd)
        
        # 5. Database Memory Injection
        log_interview_session(job_role, match_score, missing_skills, clean_resume, clean_jd)
        
        # 6. AI Brain Question Generation
        question = generate_interview_question(job_role, missing_skills)
        
        # Return the final payload to the frontend
        return {
            "status": "success",
            "match_score": match_score,
            "missing_skills": missing_skills,
            "interview_question": question
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# Add this to your imports at the top of main.py if it's not already there:
# from backend.services.ai_service import evaluate_candidate_answer

@app.post("/api/chat")
async def chat_with_recruiter(payload: ChatPayload):
    try:
        # Pass the data to the Shadow Recruiter
        feedback = evaluate_candidate_answer(payload.question, payload.answer)
        
        return {
            "status": "success",
            "feedback": feedback
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/history")
async def fetch_history():
    try:
        data = get_interview_history()
        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}