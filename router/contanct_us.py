from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.contact_us import ContactUsModel
from schemas.contact_us import ContactUsRequest

router = APIRouter()


@router.post("/contact_us")
async def contact_us(request: ContactUsRequest, db: Session = Depends(get_db)):
    # Create a new ContactUs record
    contact_us_entry = ContactUsModel(
        name=request.name,
        email=request.email,
        subject=request.subject,
        message=request.message
    )
    db.add(contact_us_entry)
    db.commit()
    db.refresh(contact_us_entry)
    return {"message": "Your query has been received. We'll get back to you soon!"}
