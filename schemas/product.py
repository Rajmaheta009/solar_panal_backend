from pydantic import BaseModel

class ProductRequest(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    is_deleted: bool = False  # Optional, default value
