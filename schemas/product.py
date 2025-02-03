from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductInResponse(ProductCreate):
    id: int
