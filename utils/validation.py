from fastapi import HTTPException, Header
from config.config import STATIC_TOKEN

async def validate_token(token: str = Header(...)):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
