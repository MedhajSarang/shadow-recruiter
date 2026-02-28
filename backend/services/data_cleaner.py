import pandas as pd
import re
import sys
import os

#Ensure Python can find our parser
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.pdf_parser import extract_text_from_pdf

def clean_text(raw_text: str) -> str:
    """Removes unnecessary whitespace, special characters, and normalizes text."""
    if not raw_text:
        return ""
    
    # 1. Convert everything to lowercase so "Python" and "PYTHON" match
    text = raw_text.lower()

    # 2. Regex: Remove weird bullet points and symbols, keep letters/numbers/basic punctuation
    text = re.sub(r'[^a-z0-9\s\.\,\+]', ' ', text)

    # 3. Regex: Replace multiple spaces and line breaks with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def structure_resume_data(raw_text: str) -> pd.DataFrame:
    """Cleans raw text and structures it into a Pandas DataFrame."""
    cleaned_text = clean_text(raw_text)

    #Pack the cleaned data into a Pandas DataFrame for easy analysis later 
    df = pd.DataFrame({
        "document_type": ["resume"],
        "cleaned_content": [cleaned_text],
        "word_count": [len(cleaned_text.split())]
    })

    return df

# ---TEST BLOCK---
if __name__ == "__main__":
    print("1. Extracting raw text using Parser.")
    
    #Go up to two levels to find the test_resume.pdf in the root folder.

    raw_text = extract_text_from_pdf("test_resume.pdf")

    print("2. Pushing text through Pandas Cleaning Pipeline...")
    df = structure_resume_data(raw_text)

    print("\n--- CLEANED PANDAS DATAFRAME---")
    print(df.to_string())
    print("\n-------------------------------")
    print("Status: Data Cleaning Complete.")