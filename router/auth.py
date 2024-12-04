from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from models.user import User
from schemas.auth import UserCreate, LoginRequest, TokenResponse, UserResponse
from database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the email is already registered
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Hash password and create user
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    # Generate JWT token
    token = create_access_token({"id": user.id, "email": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
