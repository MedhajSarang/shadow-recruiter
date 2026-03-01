import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.database import get_db_client

def log_interview_session(job_role: str, match_score: float, missing_skills: list, resume_text: str, jd_text: str, candidate_name: str = "Anonymous"):
    """Saves the interview session to Supabase, tagged with the candidate's name."""
    try:
        supabase = get_db_client()
        data = {
            "job_role": job_role,
            "match_score": match_score,
            "missing_skills": missing_skills,
            "resume_text": resume_text,
            "jd_text": jd_text,
            "candidate_name": candidate_name # New field added
        }
        response = supabase.table("interviews").insert(data).execute()
        return response.data
    except Exception as e:
        return f"Database Error: {str(e)}"

def get_interview_history(candidate_name: str):
    """Fetches the 10 most recent interview sessions for a SPECIFIC candidate."""
    try:
        supabase = get_db_client()
        # Filter by candidate_name, order by newest, limit 10
        response = supabase.table("interviews").select("*").eq("candidate_name", candidate_name).order("created_at", desc=True).limit(10).execute()
        return response.data
    except Exception as e:
        return f"Database Fetch Error: {str(e)}"