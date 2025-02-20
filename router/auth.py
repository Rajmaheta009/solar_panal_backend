from fastapi import APIRouter, Depends, HTTPException,Header
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from database import get_db
from models.user import User
from models.auth_user import AuthUser
from schemas.user import UserCreate, UserLogin, UserUpdate

router = APIRouter()

# OAuth2 dependency for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/users", response_model=list[dict])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_delete == False).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phonenumber": user.phonenumber,
            "role": user.role,
            "is_delete": user.is_delete
        }
        for user in users
    ]


@router.get("/users/{user_id}", status_code=200)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.is_delete == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phonenumber": user.phonenumber,
        "role": user.role,
        "is_delete": user.is_delete
    }


@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db),user_name:str=Header(None)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            if db_user.is_delete:
                # Reactivate the user without modifying their password
                db_user.is_delete = False
                db_user.name = user.name
                db_user.phonenumber = user.phonenumber
                db_user.role = user.role
                db.commit()
                db.refresh(db_user)
                return {"msg": "User re-registered successfully"}

            else:
                raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = hash_password(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            phonenumber=user.phonenumber,
            role=user.role,
            is_delete=user.is_delete
        )
        setattr(new_user, "current_user", user_name)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"msg": "User registered successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while registering the user")


@router.post("/login", status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if db_user.is_delete:
        raise HTTPException(status_code=404, detail="User Deleted")

    token = create_access_token({"id": db_user.id, "role": db_user.role}, db)
    return {"access_token": token, "token_type": "bearer", "role": db_user.role,"username":db_user.name}


@router.post("/logout", status_code=200)
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_in_db = db.query(AuthUser).filter(AuthUser.token == token).first()
    if token_in_db:
        db.delete(token_in_db)
        db.commit()
    return {"detail": "Successfully logged out"}


@router.put("/users/{user_id}", status_code=200)
def edit_user(user_id: int,
              user: UserUpdate,
              db: Session = Depends(get_db),
              token: str = Depends(oauth2_scheme),
              user_name:str=Header(None)
              ):

    db_user = db.query(AuthUser).filter(AuthUser.token == token).first()
    if not db_user:
        raise HTTPException(status_code=401, detail=f"{token},-----------Invalid token,")

    if db_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Permission denied")

    db_user_to_edit = db.query(User).filter(User.id == user_id).first()
    if not db_user_to_edit:
        raise HTTPException(status_code=404, detail="User not found")

    db_user_to_edit.name = user.name
    db_user_to_edit.email = user.email
    db_user_to_edit.phonenumber = user.phonenumber
    db_user_to_edit.role = user.role
    db_user_to_edit.is_delete = user.is_delete

    setattr(db_user_to_edit, "current_user", user_name)

    db.commit()
    db.refresh(db_user_to_edit)

    return {"msg": "User updated successfully","username":user_name}


@router.delete("/users/{user_id}", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme),user_name:str = Header(None)):
    db_user = db.query(AuthUser).filter(AuthUser.token == token).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid token")

    if db_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Permission denied")

    db_user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not db_user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    db_user_to_delete.is_delete = True
    setattr(db_user_to_delete, "current_user", user_name)
    db.commit()
    db.refresh(db_user_to_delete)

    return {"msg": "User deleted successfully", "is_delete": db_user_to_delete.is_delete}
