import os
import secrets
from fastapi import Header, HTTPException

def require_admin(authorization: str | None = Header(default=None)) -> None:
    expected = os.getenv("ADMIN_API_TOKEN")
    if not expected:
        raise HTTPException(status_code=503, detail="Admin authorization is not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Admin authorization required")
    if not secrets.compare_digest(expected, authorization[7:]):
        raise HTTPException(status_code=401, detail="Admin authorization required")
