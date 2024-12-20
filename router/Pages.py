from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.pages import Page
from schemas.pages import PageRequest

router = APIRouter()

def is_admin():
    return True

@router.post("/")
def create_page(request: PageRequest, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    page = Page(menu_id=request.menu_id, title=request.title)
    db.add(page)
    db.commit()
    db.refresh(page)
    return page

@router.put("/{page_id}")
def update_page(page_id: int, request: PageRequest, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    page = db.query(Page).filter(Page.id == page_id, Page.is_deleted == False).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    page.title = request.title
    db.commit()
    return page

@router.delete("/{page_id}")
def delete_page(page_id: int, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    page.is_deleted = True
    db.commit()
    return {"message": "Page deleted successfully"}
