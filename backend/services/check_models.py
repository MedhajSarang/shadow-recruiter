import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def get_allowed_models():
    print("Interrogating Google Servers for authorized models...\n")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("--- YOUR AUTHORIZED MODELS ---")
        for model in data.get('models', []):
            # We only care about models that can generate text
            if 'generateContent' in model.get('supportedGenerationMethods', []):
                print(f"✔️ {model['name']}")
        print("------------------------------")
    else:
        print(f"Connection Failed: {response.text}")

if __name__ == "__main__":
    get_allowed_models()