from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand: Mapped[str] = mapped_column(String, nullable=False)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    sku_code: Mapped[str | None] = mapped_column(String, nullable=True)
    agsk_code: Mapped[str | None] = mapped_column(String, nullable=True)
    product: Mapped[str | None] = mapped_column(String, nullable=True)
    price_ex_vat: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    price_inc_vat: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    uom: Mapped[str | None] = mapped_column(String, nullable=True)

    brand: Mapped[Brand] = relationship("Brand")
