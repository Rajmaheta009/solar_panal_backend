from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class AuthUser(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)  # Foreign key to the users table
    token = Column(String, nullable=False)
    is_deleted = Column(Integer,default=0)
