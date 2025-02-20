from database import SessionLocal
import json
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class ChangeLog(Base):
    __tablename__ = "change_logs"

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, nullable=False)  # Table that was modified
    user_name = Column(String, nullable=False)   # Who made the change
    action = Column(String, nullable=False)      # INSERT, UPDATE, DELETE
    row_id = Column(Integer)                     # ID of the affected row
    timestamp = Column(DateTime, default=func.now())  # Time of change


def log_changes(mapper, connection, target):
    """Logs INSERT and UPDATE actions dynamically for any table"""
    session = SessionLocal()

    user_name = getattr(target, "current_user", "Unknown User")  # Capture username
    table_name = target.__tablename__  # Get table name dynamically
    row_id = target.id if hasattr(target, "id") else None  # Capture primary key

    # Determine action type
    action = "INSERT"
    if row_id:
        existing_record = session.query(target.__class__).filter_by(id=row_id).first()
        action = "UPDATE" if existing_record else "INSERT"

    log_entry = ChangeLog(
        table_name=table_name,
        user_name=user_name,
        action=action,
        row_id=row_id,
    )

    session.add(log_entry)
    session.commit()
    session.close()


def log_deletes(mapper, connection, target):
    """Logs DELETE actions dynamically for any table"""
    session = SessionLocal()

    user_name = getattr(target, "current_user", "Unknown User")
    table_name = target.__tablename__
    row_id = target.id if hasattr(target, "id") else None

    log_entry = ChangeLog(
        table_name=table_name,
        user_name=user_name,
        action="DELETE",
        row_id=row_id,
        changed_data=f"Deleted row with ID {row_id}"
    )

    session.add(log_entry)
    session.commit()
    session.close()
