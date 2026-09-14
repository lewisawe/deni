"""FastAPI application entrypoint for Deni."""
from pathlib import Path

try:  # load .env if present (AT key, AWS profile); optional
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:  # noqa: BLE001
    pass

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import __version__
from . import ai, before_flow, parse_explain, recourse as recourse_mod, ussd
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


@app.post("/api/parse")
async def parse(text: str = Form(""), image: UploadFile | None = File(None)) -> dict:
    """AI-extract offer fields from a pasted SMS or an uploaded screenshot (R2)."""
    img_bytes = await image.read() if image is not None else None
    img_fmt = "png"
    if image is not None and image.filename and "." in image.filename:
        img_fmt = image.filename.rsplit(".", 1)[-1].lower()
        img_fmt = {"jpg": "jpeg"}.get(img_fmt, img_fmt)
    return parse_explain.parse_offer(text=text, image_bytes=img_bytes, image_format=img_fmt)


class ExplainIn(BaseModel):
    cost: dict
    lang: str = "en"


@app.post("/api/explain")
def explain(payload: ExplainIn) -> dict:
    """Phrase computed cost figures in EN/SW/Sheng (R11). Numbers unchanged."""
    return parse_explain.explain_cost(payload.cost, payload.lang)


@app.get("/api/ai-status")
def ai_status() -> dict:
    """Whether AI features are available (for graceful UI degradation)."""
    return {"available": ai.available()}


class RecourseIn(BaseModel):
    text: str
    lang: str = "en"


@app.post("/api/recourse")
def recourse(payload: RecourseIn) -> dict:
    """DURING/AFTER: classify a problem -> law + forum + prepared complaint (R6,R13)."""
    return recourse_mod.recourse(payload.text, payload.lang)


@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_callback(text: str = Form(""), sessionId: str = Form(""),
                        phoneNumber: str = Form(""), serviceCode: str = Form("")) -> str:
    """Africa's Talking USSD callback (R8). Returns CON/END plain text."""
    return ussd.handle(text)


# Serve the SPA. Mounted last so API routes take precedence.
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
