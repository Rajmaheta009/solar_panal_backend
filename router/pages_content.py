from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.Page_Content import PageContent
from schemas.pages_content import PageContentRequest

router = APIRouter()

def is_admin():
    return True

@router.post("/")
def create_page_content(request: PageContentRequest, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    page_content = PageContent(page_id=request.page_id, content=request.content)
    db.add(page_content)
    db.commit()
    db.refresh(page_content)
    return page_content

@router.put("/{content_id}")
def update_page_content(content_id: int, request: PageContentRequest, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    page_content = db.query(PageContent).filter(PageContent.id == content_id, PageContent.is_deleted == False).first()
    if not page_content:
        raise HTTPException(status_code=404, detail="Page content not found")
    page_content.content = request.content
    db.commit()
    return page_content

@router.delete("/{content_id}")
def delete_page_content(content_id: int, db: Session = Depends(get_db)):
    if not is_admin():
        raise HTTPException(status_code=403, detail="Access denied")
    page_content = db.query(PageContent).filter(PageContent.id == content_id).first()
    if not page_content:
        raise HTTPException(status_code=404, detail="Page content not found")
    page_content.is_deleted = True
    db.commit()
    return {"message": "Page content deleted successfully"}
