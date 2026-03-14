import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load the secret keys from the .env file
load_dotenv()

# Fetch the raw keys
raw_url = os.environ.get("SUPABASE_URL")
raw_key = os.environ.get("SUPABASE_KEY")

# Sanitize the keys (Acts like scissors: cuts off hidden spaces, enters, and accidental quotes)
url = raw_url.strip().strip('"').strip("'") if raw_url else None
key = raw_key.strip().strip('"').strip("'") if raw_key else None

def get_db_client() -> Client:
    """Initializes and returns the Supabase client."""
    if not url or not key:
        raise ValueError("CRITICAL ERROR: Supabase credentials not found in .env file or Render Environment")
    
    # We will print this to the Render logs to verify exactly what it is trying to dial
    print(f"DIAGNOSTIC - Backend dialing Supabase at: [{url}]")
    
    return create_client(url, key)

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Testing Supabase connection...")
    try:
        supabase = get_db_client()
        print("Status: Connection Successful! Supabase client initialized.")
    except Exception as e:
        print(f"Status: Connection Failed. Error: {e}")