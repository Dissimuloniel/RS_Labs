from datetime import datetime, timedelta
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

logging.basicConfig(
    filename="auth.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

pwd_context = CryptContext(schemes=["bcrypt"])

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": pwd_context.hash("secret"),
    }
}

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form.username)
    if not user or not verify_password(
        form.password, user["hashed_password"]):
        logging.warning(f"FAILED LOGIN: {form.username}")
        raise HTTPException(status_code=401, detail="Bad credentials")
    token = create_access_token({"sub": form.username})
    logging.info(f"SUCCESS LOGIN: {form.username}")
    return {"access_token": token, "token_type": "bearer"}