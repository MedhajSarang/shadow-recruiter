import os
from google import genai
from dotenv import load_dotenv

# Load the secret keys from the .env file
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("CRITICAL ERROR: GEMINI_API_KEY not found in .env")

# Initialize the official SDK client
client = genai.Client(api_key=api_key)

def generate_interview_question(job_role: str, missing_skills: list) -> str:
    """Uses the official Gemini SDK to generate a targeted technical interview question."""
    
    skills_str = ", ".join(missing_skills) if missing_skills else "advanced technical concepts"
    
    prompt = f"""
    You are an expert, strict Technical Recruiter conducting an interview for a {job_role} position.
    The candidate's resume shows they might be weak or missing experience in the following areas: {skills_str}.
    
    Your task:
    Ask ONE highly technical, challenging interview question that specifically tests their knowledge on one of these missing skills.
    Do not introduce yourself. Do not say "Hello". Just ask the question directly.
    """
    
    try:
        # Using the exact model string we verified on Google's servers
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Waking up Shadow Recruiter via Official SDK...\n")
    
    test_role = "Data Analyst"
    test_missing = ["python pandas", "sql window functions"]
    
    question = generate_interview_question(test_role, test_missing)
    
    print("--- AI GENERATED QUESTION ---")
    print(question)
    print("\n-----------------------------")
    print("Status: AI Brain Online via SDK.")