import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Shadow Recruiter", page_icon="🤖", layout="wide")

st.title("Shadow Recruiter AI 🤖")
st.markdown("Your data-driven mock interview agent.")

# 2. Sidebar for BI Metrics
with st.sidebar:
    st.header("Session Metrics")
    st.write("**Match Score:** Pending...")
    st.write("**Missing Skills:** Pending...")

# 3. Main UI - Data Ingestion Zone
st.header("Step 1: Data Ingestion")

#Split the layout into two columns
col1, col2 = st.columns(2)

with col1:
    job_url = st.text_input("Paste Job Description URL")

with col2:
    resume_pdf = st.file_uploader("Upload Your Resume (PDF):", type= ["pdf"])

# 4. The Action Button
if st.button("Initialize Shadow Recruiter"):
    if job_url and resume_pdf:
        #We will connect this to your FastAPI backend later
        st.info("Files received. Backend connection pending...")
    else:
        st.warning("Strict requirement: You must provide both a Job URL and a Resume PDF.")