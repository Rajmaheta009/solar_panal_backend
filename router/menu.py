from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.menu import Menu
from schemas.menu import MenuRequest

router = APIRouter()

# Utility function to check admin access
def is_admin():
    return True  # Replace with actual admin check

# CRUD for Menu
@router.post("/")
def create_menu(request: MenuRequest, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    menu = Menu(name=request.name)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu

@router.put("/{menu_id}")
def update_menu(menu_id: int, request: MenuRequest, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    menu = db.query(Menu).filter(Menu.id == menu_id, Menu.is_deleted == False).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu.name = request.name
    db.commit()
    return menu

@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu.is_deleted = True
    db.commit()
    return {"message": "Menu deleted successfully"}
