# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from schema import ChatRequest, ChatResponse, SignUpRequest, Token, LoginRequest
# from auth import sign_up_user, authenticate_user, verify_dummy_token,dummy_tokens_db
# from app import get_response_from_groq  # Your existing function to call the LLM model

# # Initialize FastAPI app
# app = FastAPI()

# # OAuth2 Password Bearer
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Expects the token in the Authorization header

# # Route to sign up a new user
# @app.post("/sign_up")
# async def sign_up(form_data: SignUpRequest):
#     # Call sign_up_user function from auth.py to handle user registration and token generation
#     result = sign_up_user(form_data.username, form_data.password)
#     return {"message": result["message"], "access_token": result["access_token"]}

# # Route to generate token (login)
# @app.post("/token", response_model=Token)
# async def login(form_data: LoginRequest):
#     # Authenticate user using username and password
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     # Generate and return the token if authentication is successful
#     # print(dummy_tokens_db)
#     # print(token for token, username in dummy_tokens_db.items() if username == form_data.username)
#     access_token = next((token for token, username in dummy_tokens_db.items() if username == form_data.username), None)
#     if not access_token:
#         raise HTTPException(status_code=400, detail="Token generation failed")
    
#     return {"access_token": access_token, "token_type": "bearer"}

# # Chat route that uses the dummy token for authentication
# @app.post("/chat/")
# async def chat(request: ChatRequest, username: str, password: str):
#     print(f"Received username: {username}, password: {password}")  # Debugging log

#     try:
#         # Check if username and password are valid (i.e., not None)
#         if not username or not password:
#             print("1")
#             raise HTTPException(status_code=400, detail="Username or password missing")

#         # Proceed to call the Groq model
#         print("2")
#         response = await get_response_from_groq(request.prompt)
#         print("3")
#         if response is None:
#             print("4")
#             print("Received None from Groq model")  # Debugging log
#             raise HTTPException(status_code=500, detail="Failed to get response from Groq model")

#         # Log and return the response as it is without any modifications
#         print("5")
#         print(f"Response from agent: {response}")  # Debugging log
#         print("6")
#         return {"response": response}

#     except Exception as e:
#         print("7")
#         print(f"Error during chat: {str(e)}")  # Debugging log
#         raise HTTPException(status_code=500, detail=str(e))



from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from schema import ChatRequest, ChatResponse, SignUpRequest, Token, LoginRequest
from auth import sign_up_user, authenticate_user, dummy_tokens_db 
from app import get_response_from_groq  

# Initialize FastAPI app
app = FastAPI()

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  

# Route to sign up a new user
@app.post("/sign_up")
async def sign_up(form_data: SignUpRequest):
    # Call sign_up_user function from auth.py to handle user registration and token generation
    result = sign_up_user(form_data.username, form_data.password)
    return {"message": result["message"], "access_token": result["access_token"]}

# Route to generate token (login)
@app.post("/token", response_model=Token)
async def login(form_data: LoginRequest):
    # Authenticate user using username and password
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate and return the token if authentication is successful
    access_token = next((token for token, username in dummy_tokens_db.items() if username == form_data.username), None)
    if not access_token:
        raise HTTPException(status_code=400, detail="Token generation failed")
    
    return {"access_token": access_token, "token_type": "bearer"}

# chat route to communicate with the LLM model
@app.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest, password: str, username: str):
    try:      
        # Authenticate the user using the extracted username and provided password
        if authenticate_user(username, password):
            try:
                # Use the get_response_from_groq function to get the response from the LLM model
                response = await get_response_from_groq(request.prompt)
                return {"response": response}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing chat with LLM: {str(e)}")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials or token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
