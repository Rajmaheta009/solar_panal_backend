from pydantic import BaseModel

# Product model for request and response
class Product(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductInResponse(Product):
    id: int
