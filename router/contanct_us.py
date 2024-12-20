from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import contact_us
from pydantic import BaseModel, EmailStr

router = APIRouter()

class ContactUsRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

@router.post("/contact_us")
async def contact_us(request: ContactUsRequest, db: Session = Depends(get_db)):
    # Create a new ContactUs record
    contact_us_entry = contact_us(
        name=request.name,
        email=request.email,
        subject=request.subject,
        message=request.message,
        phone=request.phone
    )
    db.add(contact_us_entry)
    db.commit()
    db.refresh(contact_us_entry)
    return {"message": "Your query has been received. We'll get back to you soon!"}
