import sys
import os

# Ensure Python can find our database client from yesterday
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db_client

def log_interview_session(job_role: str, match_score: float, missing_skills: list, resume_text: str, jd_text: str):
    """Saves the initial interview analysis to Supabase."""
    try:
        supabase = get_db_client()
        
        # Package the data into a dictionary that exactly matches our SQL columns
        data = {
            "job_role": job_role,
            "match_score": match_score,
            "missing_skills": missing_skills,
            "resume_text": resume_text,
            "jd_text": jd_text
        }
        
        # Execute the SQL INSERT command via the Supabase client
        response = supabase.table("interviews").insert(data).execute()
        
        return response.data
    except Exception as e:
        return f"Database Error: {str(e)}"

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Testing Database Insertion...\n")
    
    # 1. Define dummy data representing a user session
    test_role = "Data Analyst"
    test_score = 82.5
    test_missing = ["python", "machine learning"]
    test_resume = "I know SQL and Power BI."
    test_jd = "Looking for SQL, Power BI, Python, and Machine Learning."
    
    # 2. Fire the insertion function
    result = log_interview_session(test_role, test_score, test_missing, test_resume, test_jd)
    
    print("--- INSERTION RESULT ---")
    print(result)
    print("------------------------")
    print("Status: Data successfully saved to the cloud.")