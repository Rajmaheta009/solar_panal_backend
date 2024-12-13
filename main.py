from fastapi import FastAPI
from database import Base, engine
from router import auth, news
from fastapi.middleware.cors import CORSMiddleware
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(application.router, prefix="/application", tags=["Application"])