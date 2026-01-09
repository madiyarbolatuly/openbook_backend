from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BrandBase(BaseModel):
    brand: str


class BrandCreate(BrandBase):
    pass


class BrandOut(BrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProductBase(BaseModel):
    brand_id: int
    sku_code: str | None = None
    agsk_code: str | None = None
    product: str | None = None
    price_ex_vat: float | None = None
    price_inc_vat: float | None = None
    uom: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand_name: str
