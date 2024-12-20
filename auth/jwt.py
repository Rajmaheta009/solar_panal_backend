import secrets
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.auth_user import AuthUser

# Constants
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 dependency for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to create an access token
def create_access_token(data: dict, db: Session) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(token)

    # Save the token to the database
    user_id = data.get("id")
    if user_id is None:
        raise ValueError("User ID is required to create a token.")

    # Check if an existing token exists for the user and delete it
    existing_token = db.query(AuthUser).filter(AuthUser.id == user_id).first()
    if existing_token:
        db.delete(existing_token)
        db.commit()

    # Save the new token
    auth_user = AuthUser(id=user_id, token=token)
    db.add(auth_user)
    db.commit()

    return token

# Function to verify an access token
def verify_access_token(token: str, db: Session) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_in_db = db.query(AuthUser).filter(AuthUser.token == token).first()
        if not token_in_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency to get the current user from the database
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = verify_access_token(token, db)
    user_id = payload.get("id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# Dependency to ensure the user has admin privileges
def admin_required(user: User = Depends(get_current_user)):
    if user.role != 2:  # Assuming '2' represents the admin role
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user
