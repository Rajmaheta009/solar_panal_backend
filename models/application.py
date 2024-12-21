from sqlalchemy import Column, Integer, String,Boolean
from database import Base

class Application(Base):
    __tablename__ = "application"
    id = Column(Integer, primary_key=True, index=True)
    type=Column(String)
    InnerHtmlText=Column(String)
    is_deleted = Column(Boolean, default=False)  # Changed to Boolean for clarity


