import requests
from bs4 import BeautifulSoup
import re

def scrape_job_description(url: str) -> str:
    """Fetches and extracts raw text from a job posting URL."""
    try:
        # We use a User-Agent header so websites don't immediately block us as a basic bot.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        #Send the GET request to the website

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # This throws an error if the site blocks us (e.g. 404 or 403)

        #Parse the HTML structure
        soup = BeautifulSoup(response.text, 'html.parser')

        #Extract text specifically from paragraphs, lists, and headers
        text_elements = soup.find_all(['p', 'li', 'h1', 'h2', 'h3', 'div'])
        raw_text = " ".join([elem.get_text(separator=' ', strip = True) for elem in text_elements])

        #Basic cleanup (we will pass this to our pandas cleaner later for deep cleaning)
        clean_text = re.sub(r'\s+', ' ', raw_text).strip()

        return clean_text
    
    except Exception as e:
        return f"Failed to scrape URL. Error: {str(e)}"

# ---TEST BLOCK---
if __name__ == "__main__":
    # We test with a Wikipedia page about Data Science because it has guaranteed text and won't block us
    test_url = "https://en.wikipedia.org/wiki/Data_science"
    
    print(f"1. Attempting to scrape: {test_url}\n")
    
    result = scrape_job_description(test_url)
    
    print("--- SCRAPED TEXT (First 500 characters) ---")
    print(result[:500])
    print("\n-------------------------------------------")
    print("Status: Web Scraping Complete.")