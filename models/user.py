from sqlalchemy import Column, Integer, String, Boolean,event
from database import Base
from models.trigger_log import log_changes,log_deletes

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String(255), unique=True, index=True)  # Added length for email
    password = Column(String)
    phonenumber = Column(String)  # Changed to String for phone number
    role = Column(String, default="user")
    is_delete = Column(Boolean, default=False)  # Changed to Boolean for clarity


event.listen(User, "after_insert", log_changes)
event.listen(User, "after_update", log_changes)
event.listen(User, "after_delete", log_deletes)