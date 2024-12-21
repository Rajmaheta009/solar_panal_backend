from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
    title = Column(String(150), nullable=False)
    is_deleted = Column(Boolean, default=False)  # Changed to Boolean for clarity

    menu = relationship("Menu")
