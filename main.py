from fastapi import FastAPI
from database import Base, engine
from router import auth
from router.news import router as news_router

# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


app.include_router(news_router)
