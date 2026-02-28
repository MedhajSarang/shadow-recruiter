import streamlit as st
import requests

st.set_page_config(page_title="Shadow Recruiter", page_icon="🤖", layout="wide")

st.title("Shadow Recruiter AI 🤖")
st.markdown("Your data-driven mock interview agent.")

# Main UI - Data Ingestion Zone
st.header("Step 1: Data Ingestion")

col1, col2 = st.columns(2)

with col1:
    job_url = st.text_input("Paste Job Description URL (LinkedIn/Indeed/Wiki):")
    job_role = st.text_input("Target Job Role (e.g., Data Analyst, Backend Developer):")

with col2:
    resume_pdf = st.file_uploader("Upload Your Resume (PDF):", type=["pdf"])

# The Action Button
if st.button("Initialize Shadow Recruiter"):
    if job_url and job_role and resume_pdf:
        with st.spinner("Analyzing application... This takes about 10 seconds."):
            try:
                # Prepare the files and data for the POST request
                files = {"resume": (resume_pdf.name, resume_pdf.getvalue(), "application/pdf")}
                data = {"job_url": job_url, "job_role": job_role}
                
                # Hit the FastAPI backend
                response = requests.post("http://127.0.0.1:8000/api/analyze", data=data, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get("status") == "success":
                        st.success("Analysis Complete.")
                        
                        # Step 2: Business Intelligence Dashboard
                        st.header("Step 2: Business Intelligence")
                        
                        metrics_col, skills_col = st.columns(2)
                        
                        with metrics_col:
                            st.subheader("Match Score")
                            score = result['match_score']
                            # Ensure score is between 0 and 100 for the progress bar
                            safe_score = max(0.0, min(100.0, float(score)))
                            st.metric(label="Cosine Similarity", value=f"{safe_score}%")
                            st.progress(safe_score / 100.0)
                            
                        with skills_col:
                            st.subheader("Critical Missing Skills")
                            if result['missing_skills']:
                                for skill in result['missing_skills']:
                                    st.warning(skill.upper())
                            else:
                                st.success("No critical missing skills detected!")
                                
                        # Step 3: The Shadow Recruiter
                        st.header("Step 3: The Shadow Recruiter")
                        st.error("🚨 LIVE INTERVIEW QUESTION 🚨")
                        st.write(result['interview_question'])
                        
                    else:
                        st.error(f"Backend Error: {result.get('message')}")
                else:
                    st.error(f"Server Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: Is your FastAPI server running? Error: {e}")
    else:
        st.warning("Strict requirement: You must provide a Job URL, Job Role, and a Resume PDF.")