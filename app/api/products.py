from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.schemas import ProductCreate, ProductOut, ProductUpdate
from app.db.models import Brand, Product
from app.db.session import get_db

router = APIRouter(prefix="/api/products", tags=["products"])


def _to_product_out(p: Product) -> ProductOut:
    return ProductOut(
        id=p.id,
        brand_id=p.brand_id,
        brand_name=p.brand.brand,
        sku_code=p.sku_code,
        agsk_code=p.agsk_code,
        product=p.product,
        uom=p.uom,
        price_ex_vat=float(p.price_ex_vat) if p.price_ex_vat is not None else None,
        price_inc_vat=float(p.price_inc_vat) if p.price_inc_vat is not None else None,
    )


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).join(Brand).order_by(Product.id.asc()).all()
    return [_to_product_out(p) for p in products]


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Not found")
    # ensure relationship loaded
    _ = p.brand
    return _to_product_out(p)


@router.get("/search", response_model=list[ProductOut])
def search_products(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    q_like = f"%{q}%"

    # This mimics the .NET behavior (search in sku_code/agsk_code/product)
    products = (
        db.query(Product)
        .join(Brand)
        .filter(
            or_(
                Product.sku_code.ilike(q_like),
                Product.agsk_code.ilike(q_like),
                Product.product.ilike(q_like),
            )
        )
        .order_by(Product.id.asc())
        .all()
    )

    return [_to_product_out(p) for p in products]


@router.post("", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    brand_exists = db.query(Brand.id).filter(Brand.id == payload.brand_id).first() is not None
    if not brand_exists:
        raise HTTPException(status_code=400, detail=f"Brand with ID {payload.brand_id} does not exist.")

    # match existing behavior: if product with same brand+sku+agsk exists, return OK-ish
    existing = (
        db.query(Product)
        .filter(
            Product.brand_id == payload.brand_id,
            Product.sku_code == payload.sku_code,
            Product.agsk_code == payload.agsk_code,
        )
        .first()
    )
    if existing is not None:
        _ = existing.brand
        return _to_product_out(existing)

    p = Product(
        brand_id=payload.brand_id,
        sku_code=payload.sku_code,
        agsk_code=payload.agsk_code,
        product=payload.product,
        uom=payload.uom,
        price_ex_vat=payload.price_ex_vat,
        price_inc_vat=payload.price_inc_vat,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    _ = p.brand
    return _to_product_out(p)


@router.put("/{product_id}", status_code=204)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    if product_id != payload.id:
        raise HTTPException(status_code=400, detail="ID mismatch")

    p = db.get(Product, product_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Not found")

    p.brand_id = payload.brand_id
    p.sku_code = payload.sku_code
    p.agsk_code = payload.agsk_code
    p.product = payload.product
    p.uom = payload.uom
    p.price_ex_vat = payload.price_ex_vat
    p.price_inc_vat = payload.price_inc_vat

    db.commit()
    return None


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(p)
    db.commit()
    return None
