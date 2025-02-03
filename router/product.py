from fastapi import APIRouter, HTTPException
from typing import List
from schemas.product import ProductCreate, ProductInResponse

router = APIRouter()

# Sample in-memory database
products_db = {}

# Create Product
@router.post("/", response_model=ProductInResponse)
async def create_product(product: ProductCreate):
    product_id = len(products_db) + 1
    products_db[product_id] = product
    return {**product.dict(), "id": product_id}

# Get All Products
@router.get("/", response_model=List[ProductInResponse])
async def get_all_products():
    return [
        {**product.dict(), "id": product_id}
        for product_id, product in products_db.items()
    ]

# Get Product by ID
@router.get("/{product_id}", response_model=ProductInResponse)
async def get_product_by_id(product_id: int):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {**product.dict(), "id": product_id}

# Update Product
@router.put("/{product_id}", response_model=ProductInResponse)
async def update_product(product_id: int, product: ProductCreate):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db[product_id] = product
    return {**product.dict(), "id": product_id}

# Delete Product
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return None
