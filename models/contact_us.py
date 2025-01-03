from sqlalchemy import Column, Integer, String,Boolean
from database import Base

class contact_us(Base):
    __tablename__ = "contact_us"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    subject = Column(String)
    message = Column(String)
    ph_no = Column(Integer)
    is_deleted = Column(Boolean, default=False)  # Changed to Boolean for clarity
