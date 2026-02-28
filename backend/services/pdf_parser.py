import fitz

def extract_text_from_pdf(pdf_path: str) -> str:
    """Reads a PDF file and returns all its text as a single string."""
    extracted_text = ""

    try:
        #Open the document
        with fitz.open(pdf_path) as doc:
            #Loop through every single page in the PDF
            for page in doc:
                extracted_text += page.get_text()
        
        return extracted_text
    except Exception as e: 
        return f"Error reading PDF : {str(e)}"

# --- TEST BLOCK ---
# This block only runs if we execute this specific file directly
if __name__ == "__main__":
    #Tell the script where to find our test file
    sample_path = "test_resume.pdf"

    print("Initializing PDF Parser...\n")

    #Run the function
    result = extract_text_from_pdf("test_resume.pdf")

    print("---EXTRACTED TEXT (First 500 characters)---")
    print(result[:500])
    print("\n-----------------------------------------")
    print("Status: Extraction Complete")