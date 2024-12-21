from sqlalchemy import Column, Integer, String,Boolean
from database import Base  # Correct import for Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    picture = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)  # Changed to Boolean for clarity
