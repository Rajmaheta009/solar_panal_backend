from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String(255), unique=True, index=True)  # Added length for email
    password = Column(Integer)
    phonenumber = Column(String)  # Changed to String for phone number
    role = Column(String, default="user")
    is_delete = Column(Boolean, default=False)  # Changed to Boolean for clarity
