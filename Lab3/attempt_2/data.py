import logging
from jose import jwt, JWTError
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/login")

logging.basicConfig(
    filename="data.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)

    if not user:
        logging.warning("ACCESS DENIED")
        raise HTTPException(status_code=401, detail="Invalid token")

    logging.info(f"ACCESS GRANTED: {user}")
    return user

@app.get("/data")
async def get_data(user: str = Depends(get_current_user)):
    return {
        "message": f"Secret data for {user}",
        "data": [1, 2, 3, 4],
    }