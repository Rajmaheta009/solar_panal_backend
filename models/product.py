from requests import Session
from sqlalchemy import Column, Integer, String, Float, Boolean, text
from database import Base
from models.trigger_log import log_changes, log_deletes
from sqlalchemy import event

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

event.listen(Product, "after_insert", log_changes)
event.listen(Product, "after_update", log_changes)
event.listen(Product, "after_delete", log_deletes)

def get_next_id(db: Session):
    result = db.execute(text("SELECT nextval(pg_get_serial_sequence('products', 'id'))"))
    return result.scalar()

