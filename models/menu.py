from sqlalchemy import Column, Integer, String,Boolean
from database import Base  # Correct import for Base

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name  = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)  # Changed to Boolean for clarity
