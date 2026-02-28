import streamlit as st
import requests

st.set_page_config(page_title="Shadow Recruiter", page_icon="🤖", layout="wide")

# --- 1. THE STATE MACHINE (Memory Vault) ---
# If these variables don't exist yet, create them.
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

st.title("Shadow Recruiter AI 🤖")
st.markdown("Your data-driven mock interview agent.")

# --- 2. DATA INGESTION (Only visible before analysis) ---
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
                        
                        # Lock the results into the State Machine
                        st.session_state.match_score = result['match_score']
                        st.session_state.missing_skills = result['missing_skills']
                        st.session_state.current_question = result['interview_question']
                        
                        # Add the AI's first question to the chat history
                        st.session_state.chat_history.append({"role": "ai", "content": result['interview_question']})
                        
                        # Flip the switch to hide this form and show the dashboard
                        st.session_state.analysis_complete = True
                        st.rerun()  # Force the page to refresh immediately
                    else:
                        st.error(f"Backend Error: {response.json().get('message')}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
        else:
            st.warning("Strict requirement: Provide Job URL, Job Role, and Resume PDF.")

# --- 3. DASHBOARD & CHAT LOOP (Only visible after analysis) ---
if st.session_state.analysis_complete:
    
    # Allow the user to reset the app
    if st.sidebar.button("Start New Interview"):
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

    # Render the entire chat history from the vault
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # The Chat Input Box
    if user_answer := st.chat_input("Type your answer to the Recruiter..."):
        
        # 1. Immediately display the user's answer
        st.session_state.chat_history.append({"role": "user", "content": user_answer})
        with st.chat_message("user"):
            st.write(user_answer)
            
        # 2. Send the answer to the backend evaluation engine
        with st.chat_message("ai"):
            with st.spinner("Grading your response..."):
                try:
                    payload = {
                        "question": st.session_state.current_question,
                        "answer": user_answer
                    }
                    eval_response = requests.post("http://127.0.0.1:8000/api/chat", json=payload)
                    
                    if eval_response.status_code == 200 and eval_response.json().get("status") == "success":
                        ai_feedback = eval_response.json()["feedback"]
                        
                        # Display the grade and save it to history
                        st.write(ai_feedback)
                        st.session_state.chat_history.append({"role": "ai", "content": ai_feedback})
                    else:
                        st.error("Failed to get evaluation from backend.")
                except Exception as e:
                    st.error(f"Connection error: {e}")