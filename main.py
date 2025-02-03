from fastapi import FastAPI
from database import Base, engine
from router import auth, news,application_endpoint,contanct_us,menu,Pages,pages_content,dbsync,product
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
app.include_router(application_endpoint.router, prefix="/application", tags=["Application"])
app.include_router(contanct_us.router, prefix="/contanct_us", tags=["Application"])
app.include_router(menu.router, prefix="/api/menu", tags=["Menu"])
app.include_router(Pages.router, prefix="/api/pages", tags=["Pages"])
app.include_router(pages_content.router, prefix="/api/pages-content", tags=["Page Content"])
app.include_router(dbsync.router, prefix="/dbsync")
app.include_router(product.router, prefix="/products", tags=["products"])