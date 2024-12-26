from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.menu import Menu
from schemas.menu import MenuRequest
from auth.jwt import admin_required
from models.user import User

router = APIRouter()

# CRUD for Menu
@router.get("/", status_code=200)
def get_menu(
        db: Session = Depends(get_db),
        user: User = Depends(admin_required),
):
    menus = db.query(Menu).filter(Menu.is_deleted == False).all()
    return {"menus": menus}


@router.post("/", status_code=201)
def create_menu(
        menu: MenuRequest,
        db: Session = Depends(get_db),
        user: User = Depends(admin_required),
):
    new_menu = Menu(**menu.dict())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return {"msg": "Menu created successfully", "menu": new_menu}


@router.put("/{menu_id}", status_code=200)
def update_menu(
        menu_id: int,
        menu: MenuRequest,
        db: Session = Depends(get_db),
        user: User = Depends(admin_required),
):
    existing_menu = db.query(Menu).filter(Menu.id == menu_id, Menu.is_deleted == False).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    for key, value in menu.dict().items():
        setattr(existing_menu, key, value)
    db.commit()
    db.refresh(existing_menu)
    return {"msg": "Menu updated successfully", "menu": existing_menu}


@router.delete("/{menu_id}", status_code=200)
def delete_menu(
        menu_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(admin_required),
):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu.is_deleted = True
    db.commit()
    return {"msg": "Menu deleted successfully"}
