from fastapi import FastAPI, Header, HTTPException
from jose import jwt, JWTError
from cryptography.fernet import Fernet
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)

logging.basicConfig(
    filename="data.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None

@app.post("/log-unauthorized")
def log_unauthorized():
    logging.warning("Unauthorized access attempt from web page (no token)")
    return {"status": "logged"}

@app.get("/data")
def get_secure_data(authorization: str = Header(None, alias="Authorization")):

    logging.info("Access attempt to /data")

    if not authorization:
        logging.warning("No token provided")
        raise HTTPException(status_code=401, detail="Token required")

    token = authorization.replace("Bearer ", "")
    user = verify_token(token)

    if not user:
        logging.warning("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")

    logging.info(f"Access granted for {user}")

    secret_data = f"Very secret data for {user}"
    encrypted = cipher.encrypt(secret_data.encode())

    return {
        "massage": f"Hello, {user}! Here is your encrypted data.",
        "secret_data": secret_data,
        "encrypted_data": encrypted.decode(),
        "encryption_key": FERNET_KEY.decode()
    }
