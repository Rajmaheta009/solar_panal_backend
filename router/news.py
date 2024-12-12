from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.news import NewsCreate, NewsResponse
from services.news import create_news, get_all_news, get_news_by_id, update_news, delete_news
from auth.jwt import admin_required  # Assuming admin role is validated here

router = APIRouter(tags=["News"], prefix="/news")

# Ensure only admins can access
def admin_required(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")

@router.post("/", response_model=NewsResponse, dependencies=[Depends(admin_required)])
def create_news_endpoint(news: NewsCreate, db: Session = Depends(get_db)):
    return create_news(db, news)

@router.get("/", response_model=list[NewsResponse])
def get_news_endpoint(db: Session = Depends(get_db)):
    return get_all_news(db)

@router.get("/{news_id}", response_model=NewsResponse)
def get_news_by_id_endpoint(news_id: int, db: Session = Depends(get_db)):
    news = get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.put("/{news_id}", response_model=NewsResponse, dependencies=[Depends(admin_required)])
def update_news_endpoint(news_id: int, news: NewsCreate, db: Session = Depends(get_db)):
    updated_news = update_news(db, news_id, news)
    if not updated_news:
        raise HTTPException(status_code=404, detail="News not found")
    return updated_news

@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_required)])
def delete_news_endpoint(news_id: int, db: Session = Depends(get_db)):
    if not delete_news(db, news_id):
        raise HTTPException(status_code=404, detail="News not found")
