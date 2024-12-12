from sqlalchemy.orm import Session
from models.news import News
from schemas.news import NewsCreate

def create_news(db: Session, news: NewsCreate):
    new_news = News(**news.dict())
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return new_news

def get_all_news(db: Session):
    return db.query(News).all()

def get_news_by_id(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()

def update_news(db: Session, news_id: int, news: NewsCreate):
    existing_news = db.query(News).filter(News.id == news_id).first()
    if existing_news:
        for key, value in news.dict().items():
            setattr(existing_news, key, value)
        db.commit()
        db.refresh(existing_news)
        return existing_news
    return None

def delete_news(db: Session, news_id: int):
    existing_news = db.query(News).filter(News.id == news_id).first()
    if existing_news:
        db.delete(existing_news)
        db.commit()
        return True
    return False
