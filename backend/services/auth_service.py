import sys
import os
from passlib.context import CryptContext

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.database import get_db_client

# Define the encryption algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(username: str, password: str):
    """Hashes the password and creates a new user in Supabase."""
    try:
        supabase = get_db_client()
        
        # 1. Check if user already exists
        existing = supabase.table("users").select("*").eq("username", username).execute()
        if existing.data:
            return {"status": "error", "message": "Username already taken."}
        
        # 2. Enforce bcrypt's 72-byte limit
        safe_password = password[:72]
        
        # 3. Hash the password
        hashed_pw = pwd_context.hash(safe_password)
        
        # 4. Save to database
        supabase.table("users").insert({"username": username, "password_hash": hashed_pw}).execute()
        return {"status": "success", "message": "Registration successful."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def authenticate_user(username: str, password: str):
    """Verifies the plain-text password against the hashed password in the database."""
    try:
        supabase = get_db_client()
        
        # 1. Find the user
        response = supabase.table("users").select("*").eq("username", username).execute()
        if not response.data:
            return {"status": "error", "message": "User not found."}
        
        user = response.data[0]
        
        # 2. Enforce bcrypt's 72-byte limit
        safe_password = password[:72]
        
        # 3. Verify the mathematical hash
        if pwd_context.verify(safe_password, user["password_hash"]):
            return {"status": "success", "message": "Authentication successful."}
        else:
            return {"status": "error", "message": "Incorrect password."}
    except Exception as e:
        return {"status": "error", "message": str(e)}