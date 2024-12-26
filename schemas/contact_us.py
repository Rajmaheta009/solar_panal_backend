from pydantic import BaseModel, EmailStr
class ContactUsRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str