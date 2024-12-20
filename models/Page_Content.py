from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class PageContent(Base):
    __tablename__ = "pages_content"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False)

    page = relationship("Page")
