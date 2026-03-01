import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Shadow Recruiter", page_icon="🤖", layout="wide")

# --- STATE MACHINE ---
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
if "match_score" not in st.session_state:
    st.session_state.match_score = 0
if "missing_skills" not in st.session_state:
    st.session_state.missing_skills = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  
if "current_question" not in st.session_state:
    st.session_state.current_question = ""

# --- NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Mock Interview", "Interview History"])

st.title("Shadow Recruiter AI 🤖")

# ==========================================
# PAGE 1: MOCK INTERVIEW (Your existing code)
# ==========================================
if page == "Mock Interview":
    st.markdown("Your data-driven mock interview agent.")

    if not st.session_state.analysis_complete:
        st.header("Step 1: Data Ingestion")
        col1, col2 = st.columns(2)

        with col1:
            job_url = st.text_input("Paste Job Description URL:")
            job_role = st.text_input("Target Job Role:")

        with col2:
            resume_pdf = st.file_uploader("Upload Your Resume (PDF):", type=["pdf"])

        if st.button("Initialize Shadow Recruiter"):
            if job_url and job_role and resume_pdf:
                with st.spinner("Analyzing application... This takes about 10 seconds."):
                    try:
                        files = {"resume": (resume_pdf.name, resume_pdf.getvalue(), "application/pdf")}
                        data = {"job_url": job_url, "job_role": job_role}
                        
                        response = requests.post("http://127.0.0.1:8000/api/analyze", data=data, files=files)
                        
                        if response.status_code == 200 and response.json().get("status") == "success":
                            result = response.json()
                            st.session_state.match_score = result['match_score']
                            st.session_state.missing_skills = result['missing_skills']
                            st.session_state.current_question = result['interview_question']
                            st.session_state.chat_history.append({"role": "ai", "content": result['interview_question']})
                            st.session_state.analysis_complete = True
                            st.rerun()
                        else:
                            st.error(f"Backend Error: {response.json().get('message')}")
                    except Exception as e:
                        st.error(f"Connection Failed: {e}")
            else:
                st.warning("Strict requirement: Provide Job URL, Job Role, and Resume PDF.")

    if st.session_state.analysis_complete:
        if st.sidebar.button("Reset Current Interview"):
            st.session_state.clear()
            st.rerun()

        st.header("Step 2: Business Intelligence")
        metrics_col, skills_col = st.columns(2)
        
        with metrics_col:
            st.subheader("Match Score")
            safe_score = max(0.0, min(100.0, float(st.session_state.match_score)))
            st.metric(label="Cosine Similarity", value=f"{safe_score}%")
            st.progress(safe_score / 100.0)
            
        with skills_col:
            st.subheader("Critical Missing Skills")
            if st.session_state.missing_skills:
                for skill in st.session_state.missing_skills:
                    st.warning(skill.upper())
            else:
                st.success("No critical missing skills detected!")

        st.header("Step 3: The Interview")
        st.markdown("---")

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if user_answer := st.chat_input("Type your answer to the Recruiter..."):
            st.session_state.chat_history.append({"role": "user", "content": user_answer})
            with st.chat_message("user"):
                st.write(user_answer)
                
            with st.chat_message("ai"):
                with st.spinner("Grading your response..."):
                    try:
                        payload = {"question": st.session_state.current_question, "answer": user_answer}
                        eval_response = requests.post("http://127.0.0.1:8000/api/chat", json=payload)
                        
                        if eval_response.status_code == 200 and eval_response.json().get("status") == "success":
                            ai_feedback = eval_response.json()["feedback"]
                            st.write(ai_feedback)
                            st.session_state.chat_history.append({"role": "ai", "content": ai_feedback})
                        else:
                            st.error("Failed to get evaluation from backend.")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

# ==========================================
# PAGE 2: INTERVIEW HISTORY (The New Code)
# ==========================================
elif page == "Interview History":
    st.header("Your Historical Performance")
    st.markdown("Review your past technical assessments stored in Supabase.")
    
    if st.button("Fetch Latest Data"):
        with st.spinner("Pulling records from cloud database..."):
            try:
                response = requests.get("http://127.0.0.1:8000/api/history")
                if response.status_code == 200 and response.json().get("status") == "success":
                    data = response.json()["data"]
                    
                    if not data:
                        st.info("No interview history found yet. Go crush a mock interview!")
                    else:
                        # Convert the raw JSON from Supabase into a clean Pandas DataFrame
                        df = pd.DataFrame(data)
                        
                        # Clean up the timestamp for readability
                        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                        
                        # Select and rename columns for the UI
                        display_df = df[['created_at', 'job_role', 'match_score', 'missing_skills']]
                        display_df.columns = ['Date', 'Job Role', 'Match Score (%)', 'Missing Skills Detected']
                        
                        st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    st.error("Failed to retrieve data from backend.")
            except Exception as e:
                st.error(f"Connection Failed: {e}")