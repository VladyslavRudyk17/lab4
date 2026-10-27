from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

API_KEYS = {
    "admin-key-123": "admin",
    "user-key-456": "user"
}

def get_role(api_key: str = Security(API_KEY_HEADER)):
    if not api_key or api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Недійсний або відсутній X-API-Key")
    return API_KEYS[api_key]

def require_admin(role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Доступ заборонено. Потрібні права Admin.")
    return role