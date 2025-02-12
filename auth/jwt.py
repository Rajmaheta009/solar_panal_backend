from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.auth_user import AuthUser
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Constants
SECRET_KEY ="pFL1Y_0ID6aZqk7c6pw1vZ8O-XWXFHMi4WHLJ8h42P7Mx-6-uD4uPAqTX7Lv-EJ4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20000

# OAuth2 dependency for to              ken extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Function to create an access token
def create_access_token(data: dict, db: Session) -> str:
    if not data.get("id"):
        raise ValueError("User ID is required to create a token.")
    if not data.get("role"):
        raise ValueError("role is not in ")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Save the token to the database
    user_id = data.get("id")
    user_role = data.get("role")
    # Check if an existing token exists for the user and delete it
    existing_token = db.query(AuthUser).filter(AuthUser.id == user_id).first()
    if existing_token:
        db.delete(existing_token)
        db.commit()

    # Save the new token
    auth_user = AuthUser(id=user_id, token=token,role=user_role)
    db.add(auth_user)
    db.commit()

    return token

# Function to verify an access token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        if "id" not in payload:
            raise JWTError("Payload missing 'id'")

        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.error(f"JWT verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency to get the current user from the database
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        logger.debug(f"Received token: {token}")
        payload = verify_access_token(token)
        logger.debug(f"Payload from token: {payload}")
        user_id = payload.get("id")
        if not user_id:
            logger.error("Token payload missing 'id'")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        logger.debug(f"Authenticated user: {user.name}")
        return user

    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while validating credentials",
        )

# Dependency to ensure the user has admin privileges
def admin_required(user: User = Depends(get_current_user)):
    if user.role.lower() != "admin":  # Assuming '2' represents the admin role
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user