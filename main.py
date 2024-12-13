from fastapi import FastAPI
from database import Base, engine
from router import auth
from router import news

# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(news.router, prefix="/logout", tags=["logout"])