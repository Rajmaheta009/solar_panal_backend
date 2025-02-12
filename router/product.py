from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from schemas.product import ProductRequest
from auth.jwt import admin_required
from models.user import User

router = APIRouter()


@router.get("/{product_id}", status_code=200)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"product": product}

# Get All Products (Admin Only)
@router.get("/", status_code=200)
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_deleted == False).all()
    return {"products": products}

# Create Product (Admin Only)
@router.post("/", status_code=201)
def create_product(
        product: ProductRequest,
        db: Session = Depends(get_db),
):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"msg": "Product created successfully", "product": new_product}


# Update Product (Admin Only)
@router.put("/{product_id}", status_code=200)
def update_product(
        product_id: int,
        product: ProductRequest,
        db: Session = Depends(get_db),
):
    existing_product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(existing_product, key, value)
    db.commit()
    db.refresh(existing_product)

    return {"msg": "Product updated successfully", "product": existing_product}


# Soft Delete Product (Admin Only)
@router.delete("/{product_id}", status_code=200)
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_deleted = True
    db.commit()
    return {"msg": "Product deleted successfully"}
