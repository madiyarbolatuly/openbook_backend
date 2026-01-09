from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import brands, importer, products
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="gq-kp-fastapi", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"],
)


@app.on_event("startup")
def _create_tables() -> None:
    # For a quick start this auto-creates tables.
    # For production use Alembic migrations (included).
    Base.metadata.create_all(bind=engine)


app.include_router(brands.router)
app.include_router(products.router)
app.include_router(importer.router)

@app.post("/import-data/")
async def import_data(data: dict):
    # Process the incoming data here
    # This is just an example of how you might start to handle the data
    for sheet in data.get("sheets", []):
        sheet_name = sheet.get("sheet")
        rows = sheet.get("rows")
        created = sheet.get("created")
        skipped = sheet.get("skipped")
        
        # Here you would add your logic to handle each sheet
        # For example, you might want to import the data into your database
        # or perform some other processing on it

    return {"message": "Data processed successfully"}
