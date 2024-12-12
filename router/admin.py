from fastapi import APIRouter, Depends, HTTPException
from auth.jwt import verify_access_token

router = APIRouter(tags=["Admin"], prefix="/admin")

def get_current_admin(token: str):
    payload = verify_access_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return payload

@router.get("/dashboard")
def admin_dashboard(token: str = Depends(get_current_admin)):
    return {"message": "Welcome to the admin dashboard!"}
