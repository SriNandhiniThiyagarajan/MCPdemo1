from pydantic import BaseModel
from typing import List

# Pydantic model for the request body for Chat
class ChatRequest(BaseModel):
    prompt: str 
# Pydantic model for the response body
class ChatResponse(BaseModel):
    response: str 

# Pydantic models for login and sign up
class LoginRequest(BaseModel):
    username: str
    password: str

class SignUpRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
