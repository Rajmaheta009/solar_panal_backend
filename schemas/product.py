from datetime import datetime

from pydantic import BaseModel

class ProductRequest(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    type:str
    is_deleted: bool = False  # Optional, default value

# 📜 Log Schema
class LogResponse(BaseModel):
    id: int
    table_name:str
    user_name: str
    action: str
    time: datetime