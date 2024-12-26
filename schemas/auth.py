from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phonenumber: str  # Changed to string for better compatibility
    role: str = "user"  # Default role for normal users
    is_delete : bool = False

class UserLogin(BaseModel):
    email: EmailStr  # Using EmailStr to validate email format
    password: str
