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
from . import ai, before_flow, parse_explain, receipt as receipt_mod, recourse as recourse_mod, ussd, whatsapp
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


@app.get("/api/rights")
def list_rights(country: str = "ke") -> dict:
    """Browsable know-your-rights library (access to information).

    Lets a citizen read what the law says and which public body handles it, before
    they have a problem. Every entry is sourced and dated.
    """
    from .data_pack import list_rights as _list_rights
    return _list_rights(country)


@app.get("/api/check-lender")
def check_lender(name: str = "", country: str = "ke") -> dict:
    """Check a lender against CBK's licensed Digital Credit Providers register."""
    from .data_pack import check_lender as _check_lender
    return _check_lender(country, name)


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
    country: str = "ke"


@app.post("/api/recourse")
def recourse(payload: RecourseIn) -> dict:
    """DURING/AFTER: classify a problem -> law + forum + prepared complaint (R6,R13)."""
    return recourse_mod.recourse(payload.text, payload.lang, payload.country)


class ReceiptIn(BaseModel):
    kind: str  # "cost" | "recourse"
    data: dict
    lang: str = "en"


@app.post("/api/receipt")
def make_receipt(payload: ReceiptIn) -> dict:
    """Build a shareable Deni report (the action+receipt the user keeps)."""
    if payload.kind == "cost":
        return receipt_mod.cost_receipt(payload.data, payload.lang)
    if payload.kind == "recourse":
        return receipt_mod.recourse_receipt(payload.data)
    raise HTTPException(status_code=400, detail="kind must be 'cost' or 'recourse'")


@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_callback(text: str = Form(""), sessionId: str = Form(""),
                        phoneNumber: str = Form(""), serviceCode: str = Form("")) -> str:
    """Africa's Talking USSD callback (R8). Returns CON/END plain text."""
    return ussd.handle(text)


class WhatsAppIn(BaseModel):
    sender: str
    message: str


@app.post("/webhook/whatsapp")
def whatsapp_webhook(payload: WhatsAppIn) -> dict:
    """WhatsApp inbound webhook (R8), same menu engine as USSD, turn-based.
    A provider (AT WhatsApp / Meta Cloud API / Twilio) would POST here; we reply."""
    return {"reply": whatsapp.handle_message(payload.sender, payload.message)}


# Serve the SPA. Mounted last so API routes take precedence.
if FRONTEND_DIR.is_dir():
    @app.get("/")
    def landing() -> FileResponse:
        """Marketing/landing page (civic pitch, converts to the app)."""
        return FileResponse(str(FRONTEND_DIR / "landing.html"))

    @app.get("/app")
    def app_page() -> FileResponse:
        """The Deni tool (rights / lender / cost / action)."""
        return FileResponse(str(FRONTEND_DIR / "index.html"))

    # Static assets (styles.css, app.js, and direct file access). Mounted at /static
    # AND at / for asset files; explicit routes above take precedence for / and /app.
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
