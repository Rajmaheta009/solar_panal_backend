from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from database import Base

class AuthUser(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)  # Foreign key to the users table
    token = Column(String, nullable=False)
    role = Column(String)
    is_deleted = Column(Boolean, default=False)  # Changed to Boolean for clarity
