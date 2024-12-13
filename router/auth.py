from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from database import get_db
from models.user import User
from models.auth_user import AuthUser
from schemas.auth import UserCreate, UserLogin

router = APIRouter()

# OAuth2 dependency for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        number=user.number,  # Assuming you meant "ph_no" as "number"
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    return {"msg": "User registered successfully"}

@router.post("/login", status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create a token and save it in the auth_user table
    token = create_access_token({"id": db_user.id, "role": db_user.role}, db)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout", status_code=200)
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Delete the token from the database
    token_in_db = db.query(AuthUser).filter(AuthUser.token == token).first()
    if token_in_db:
        db.delete(token_in_db)
        db.commit()
    return {"detail": "Successfully logged out"}
