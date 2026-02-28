import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load the secret keys from the .env file
load_dotenv()

# Fetch the keys
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

def get_db_client() -> Client:
    """Initializes and returns the Supabase client."""
    if not url or not key:
        raise ValueError("CRITICAL ERROR: Supabase credentials not found in .env file")
    return create_client(url, key)

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Testing Supabase connection...")
    try:
        supabase = get_db_client()
        print("Status: Connection Successful! Supabase client initialized.")
    except Exception as e:
        print(f"Status: Connection Failed. Error: {e}")