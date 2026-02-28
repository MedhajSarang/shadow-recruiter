import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text: str, job_description: str) -> float:
    """Converts text to vectors and calculates Cosine Similarity for a match score."""
    if not resume_text or not job_description:
        return 0.0

    # 1. Initialize Vectorizer (removes filler words like 'the', 'and')
    vectorizer = TfidfVectorizer(stop_words='english')

    # 2. Fit and transform the texts into a numerical matrix
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])

    # 3. Calculate the distance between the Resume Vector [0] and Job Vector [1]
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # 4. Extract the raw float and convert to a percentage
    match_score = similarity_matrix[0][0] * 100

    return round(match_score, 2)

def extract_missing_keywords(resume_text: str, job_description: str) -> list:
    """Uses TF-IDF weights to find the most critical missing skills."""
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Analyze the job description to find the most "weighted" words
    tfidf_matrix = vectorizer.fit_transform([job_description])
    feature_names = vectorizer.get_feature_names_out()
    
    # Map each word to its importance score
    word_weights = dict(zip(feature_names, tfidf_matrix.toarray()[0]))
    
    # Sort words from highest importance to lowest
    sorted_job_words = sorted(word_weights.items(), key=lambda x: x[1], reverse=True)
    
    missing_skills = []
    resume_text_lower = resume_text.lower()
    
    # Find the top 5 most important words that are missing from the resume
    for word, weight in sorted_job_words:
        # Ignore raw numbers and check if the word is absent
        if word not in resume_text_lower and not word.isnumeric():
            missing_skills.append(word)
            if len(missing_skills) >= 5:
                break
                
    return missing_skills

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Initializing ML Engine...\n")
    
    # Dummy data to test the mathematical logic
    sample_resume = "I am a backend developer skilled in python, sql, and pandas. I use flask."
    sample_jd = "Looking for a backend developer. Must have strong python, sql, fastapi, docker, and AWS."
    
    score = calculate_match_score(sample_resume, sample_jd)
    missing = extract_missing_keywords(sample_resume, sample_jd)
    
    print("--- ML ANALYSIS RESULTS ---")
    print(f"Match Score: {score}%")
    print(f"Top Missing Keywords: {missing}")
    print("---------------------------")
    print("Status: ML Engine Complete.")