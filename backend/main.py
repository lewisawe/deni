"""FastAPI application entrypoint for Deni."""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import __version__
from . import before_flow
from .data_pack import load_pack

app = FastAPI(title="Deni", version=__version__)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/health")
def health() -> dict:
    """Liveness check."""
    return {"status": "ok", "service": "deni", "version": __version__}


@app.get("/api/products")
def list_products(country: str = "ke") -> dict:
    """List modelled products for the before-flow picker."""
    pack = load_pack(country)
    return {"products": [
        {"id": p["id"], "label": p["label"], "category": p["category"]}
        for p in pack["products"]["products"]
    ]}


@app.get("/api/evaluate/{product_id}")
def evaluate(product_id: str, country: str = "ke") -> dict:
    """BEFORE assessment for a known product (cost + licence + risk + alternative)."""
    try:
        return before_flow.evaluate_product(country, product_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


class OfferIn(BaseModel):
    principal: float
    term_days: int
    repay_total: float | None = None
    deposit: float = 0
    instalment_amount: float = 0
    instalment_frequency: str = "monthly"
    num_instalments: int = 0
    extra_fees: float = 0


@app.post("/api/cost")
def cost(offer: OfferIn) -> dict:
    """BEFORE assessment for a raw offer the user enters."""
    try:
        return before_flow.evaluate_offer(**offer.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# Serve the SPA. Mounted last so API routes take precedence.
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
