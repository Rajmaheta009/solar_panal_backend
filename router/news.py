from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.jwt import verify_access_token
from database import get_db
from models.news import News
from schemas.news import NewsCreate

router = APIRouter()

def admin_required(token: str):
    payload = verify_access_token(token)
    if not payload or payload.get("role") != 1:
        raise HTTPException(status_code=403, detail="Admin access required")

@router.post("/news", dependencies=[Depends(admin_required)],status_code=201)
def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    new_news = News(title=news.title, description=news.description, picture=news.picture)
    db.add(new_news)
    db.commit()
    return {"msg": "News created successfully"}

@router.get("/news",status_code=200)
def get_news(db: Session = Depends(get_db)):
    return db.query(News).all()

@router.put("/news/{news_id}", dependencies=[Depends(admin_required)],status_code=202)
def update_news(news_id: int, news: NewsCreate, db: Session = Depends(get_db)):
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    db_news.title = news.title
    db_news.description = news.description
    db_news.picture = news.picture
    db.commit()
    return {"msg": "News updated successfully"}

@router.delete("/news/{news_id}", dependencies=[Depends(admin_required)])
def delete_news(news_id: int, db: Session = Depends(get_db)):
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    db.delete(db_news)
    db.commit()
    return {"msg": "News deleted successfully"}

