from pydantic import BaseModel
from typing import Optional

class AuthUserBase(BaseModel):
    id: int
    token: str
    role: Optional[str] = None
    is_deleted: Optional[bool] = False

class AuthUserCreate(AuthUserBase):
    pass  # Can add extra validation for token creation if needed

class AuthUserResponse(AuthUserBase):
    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy compatibility
