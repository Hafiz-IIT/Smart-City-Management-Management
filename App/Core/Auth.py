from __future__ import annotations

import hmac
import os

from fastapi import Header, HTTPException


def require_admin(x_admin_key: str = Header(default="")) -> None:
    expected = os.getenv("ADMIN_API_KEY", "")
    if len(expected.encode("utf-8")) < 32:
        raise HTTPException(status_code=503, detail="Administrative API key is not configured")
    if not hmac.compare_digest(x_admin_key, expected):
        raise HTTPException(status_code=401, detail="Valid X-Admin-Key header required")
