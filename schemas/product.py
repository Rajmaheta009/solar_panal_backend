from pydantic import BaseModel

class ProductRequest(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    type:str
    is_deleted: bool = False  # Optional, default value
