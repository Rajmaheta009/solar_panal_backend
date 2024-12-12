from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    ph_no: str
    role: int = 0

class UserLogin(BaseModel):
    email: str
    password: str
