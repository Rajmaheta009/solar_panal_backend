from sqlalchemy import Column, Integer, String,Boolean
from database import Base

class ContactUsModel(Base):
    __tablename__ = "contact_us"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    subject = Column(String)
    message = Column(String)
    is_deleted = Column(Boolean, default=False)  # Changed to Boolean for clarity
