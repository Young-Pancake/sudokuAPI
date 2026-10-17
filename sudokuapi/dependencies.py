import secrets
from typing import Annotated
from fastapi import Header, HTTPException
from .env_variables import API_KEY

async def require_api_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key is None or not secrets.compare_digest(x_api_key, str(API_KEY)):
        raise HTTPException(status_code=401, detail="invalid or missing API key")