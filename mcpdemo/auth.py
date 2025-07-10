import random
import string
from passlib.context import CryptContext
from fastapi import HTTPException
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Password hashing context (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake users database (Replace this with real DB in production)
fake_users_db = {}

# Dummy tokens DB (where we store tokens associated with users)
dummy_tokens_db = {}

# Function to hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if user and verify_password(password, user['password']):
        return user
    return None

# Function to generate a simple access token (dummy token)
def generate_access_token(username: str) -> str:
    # For simplicity, we generate a random string as a dummy token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    dummy_tokens_db[token] = username  # Save the token and associated username in a dummy DB
    return token

# Function to sign up (register) a new user
def sign_up_user(username: str, password: str):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password and store the user
    hashed_password = hash_password(password)
    fake_users_db[username] = {"username": username, "password": hashed_password}
    
    # Generate and store a dummy token for the user
    access_token = generate_access_token(username)
    return {"message": "User created successfully", "access_token": access_token}

def verify_dummy_token(token: str) -> str:
    # If the token exists in the dummy DB, return the associated username
    if token in dummy_tokens_db:
        return dummy_tokens_db[token]
    else:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
