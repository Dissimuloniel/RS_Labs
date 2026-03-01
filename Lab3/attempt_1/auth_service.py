from fastapi import FastAPI, HTTPException
from jose import jwt
from datetime import datetime, timedelta
import logging
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

users_db = {
    "admin": "password123"
}

class LoginRequest(BaseModel):
    username: str
    password: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    filename="auth.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(data: LoginRequest):
    username = data.username
    password = data.password
    logging.info(f"Login attempt: {username}")
    if users_db.get(username) != password:
        logging.warning(f"FAILED login: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(username)
    logging.info(f"SUCCESS login: {username}")
    return {"access_token": token}
