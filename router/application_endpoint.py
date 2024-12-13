from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.application import Application  # Import your Application model
from schemas.application import ApplicationCreate, ApplicationUpdate  # Schemas for validation
from auth.jwt import admin_required  # Ensure admin-only access
from models.user import User  # User model for dependency

router = APIRouter()

# Create a new application
@router.post("/", status_code=201)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
):
    new_application = Application(**application.dict())
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return {"msg": "Application created successfully", "application": new_application}

# Get all applications
@router.get("/", status_code=200)
def get_applications(
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
):
    applications = db.query(Application).all()
    return {"applications": applications}

# Update an application
@router.put("/{application_id}", status_code=200)
def update_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
):
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    for key, value in application.dict(exclude_unset=True).items():
        setattr(db_application, key, value)
    db.commit()
    db.refresh(db_application)
    return {"msg": "Application updated successfully", "application": db_application}

# Delete an application
@router.delete("/{application_id}", status_code=200)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
):
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(db_application)
    db.commit()
    return {"msg": "Application deleted successfully"}
