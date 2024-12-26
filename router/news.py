from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from auth.jwt import verify_access_token
from database import get_db
from models.news import News
from schemas.news import NewsCreate, NewsResponse

router = APIRouter()

# Dependency for verifying admin access
def admin_required(
    authorization: str = Header(..., description="Authorization token in the format 'Bearer <token>'"),
    db: Session = Depends(get_db)
):
    # Extract the token from the Authorization header
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    # Verify the token
    payload = verify_access_token(token)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

# Endpoint to get all news
@router.get("/news", status_code=200, response_model=list[NewsResponse])
def get_news(db: Session = Depends(get_db)):
    news = db.query(News).all()
    if not news:
        raise HTTPException(status_code=404, detail="No news found")
    return news

# Endpoint to create a news entry (admin-only)
@router.post("/news", status_code=201, response_model=NewsResponse, dependencies=[Depends(admin_required)])
def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    new_news = News(title=news.title, description=news.description, picture=news.picture)
    db.add(new_news)
    db.commit()
    db.refresh(new_news)  # Refresh to get the auto-generated ID
    return new_news
