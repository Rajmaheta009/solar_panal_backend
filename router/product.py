import os
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File,Header
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product,get_next_id
router = APIRouter()



UPLOAD_DIR = "uploads/products"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

@router.get("/{product_id}", status_code=200)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    image_url = f"http://127.0.0.1:8000/static/{product.image}" if product.image else None
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "stock": product.stock,
        "price": product.price,
        "type": product.type,
        "image": image_url,
        "is_deleted": product.is_deleted,  # Add any other fields you need

    }# Get All Products (Admin Only)
@router.get("/", status_code=200)
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_deleted == False).all()

    # Modify products list to include all fields, including image URLs
    product_list = []
    for product in products:
        image_url = f"http://127.0.0.1:8000/static/{product.image}" if product.image else None
        product_list.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "stock": product.stock,
            "price": product.price,
            "type": product.type,
            "image": image_url,
            "is_deleted": product.is_deleted,  # Add any other fields you need
        })

    return {"products": product_list}

# Create Product (Admin Only)
@router.post("/", status_code=201)
async def create_product(
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        stock: int = Form(...),
        type: str = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db),
        user_name : str =Header(None)
):
    file_extension = os.path.splitext(image.filename)[1] # Keeps original extension
    next_id=get_next_id(db)
    new_filename = f"{next_id}{file_extension}"  # e.g., 'product_name.jpg'

    # Define full image path
    image_path = os.path.join(UPLOAD_DIR, new_filename)
    # Save Image
    with open(image_path, "wb") as f:
        f.write(image.file.read())
    # Create Product
    new_product = Product(
        id=next_id,
        image=str(new_filename),
        name=name,
        description=description,
        price=price,
        stock=stock,
        type=type
    )

    # ✅ Attach username to product before insert (so the trigger can use it)
    setattr(new_product, "current_user", user_name)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"msg": "Product created successfully", "product": new_product,"username":user_name}


@router.put("/{product_id}", status_code=200)
def update_product(
        product_id: int,
        name: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        price: Optional[float] = Form(None),
        stock: Optional[int] = Form(None),
        type: Optional[str] = Form(None),
        image: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db),
        user_name:str = Header(None)
):
    existing_product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if name:
        existing_product.name = name
    if description:
        existing_product.description = description
    if price:
        existing_product.price = price
    if stock:
        existing_product.stock = stock
    if type:
        existing_product.type = type

    if image:
        file_extension = os.path.splitext(image.filename)[1]
        new_filename = f"{product_id}{file_extension}"
        image_path = os.path.join(UPLOAD_DIR, new_filename)

        with open(image_path, "wb") as f:
            f.write(image.file.read())

        existing_product.image = new_filename
    try:
        setattr(existing_product, "current_user", user_name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db.commit()
    db.refresh(existing_product)

    return {"msg": "Product updated successfully", "product": existing_product,"username":user_name}

# Soft Delete Product (Admin Only)
@router.delete("/{product_id}", status_code=200)
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        user_name:str = Header(None)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    setattr(product, "current_user", user_name)
    product.is_deleted = True
    db.commit()
    return {"msg": "Product deleted successfully"}
