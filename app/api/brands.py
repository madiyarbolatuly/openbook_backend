from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import BrandCreate, BrandOut
from app.db.models import Brand
from app.db.session import get_db

router = APIRouter(prefix="/api/brands", tags=["brands"])


@router.get("", response_model=list[BrandOut])
def list_brands(db: Session = Depends(get_db)):
    return db.query(Brand).order_by(Brand.id.asc()).all()


@router.get("/{brand_id}", response_model=BrandOut)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.get(Brand, brand_id)
    if brand is None:
        raise HTTPException(status_code=404, detail="Not found")
    return brand


@router.post("", response_model=BrandOut, status_code=201)
def create_brand(payload: BrandCreate, db: Session = Depends(get_db)):
    brand = Brand(brand=payload.brand)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@router.put("/{brand_id}", status_code=204)
def update_brand(brand_id: int, payload: BrandCreate, db: Session = Depends(get_db)):
    brand = db.get(Brand, brand_id)
    if brand is None:
        raise HTTPException(status_code=404, detail="Not found")

    brand.brand = payload.brand
    db.commit()
    return None


@router.delete("/{brand_id}", status_code=204)
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.get(Brand, brand_id)
    if brand is None:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(brand)
    db.commit()
    return None
