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


@app.exception_handler(FileNotFoundError)
def _missing_pack_handler(_request, exc: FileNotFoundError):
    """An unknown country code (e.g. ?country=zz) means load_pack can't find a data
    pack. Return a clean 404 instead of a 500 stack trace, so a mistyped or probed
    country is handled gracefully across every endpoint that loads a pack."""
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=404, content={"detail": str(exc) or "Unknown country pack"})


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


@app.get("/api/sources")
def sources(country: str = "ke", verify: bool = False) -> dict:
    """Civic data-health: how many sourced claims back this country pack, when the
    pack was last updated, and (with verify=true) whether every source URL is live.

    Turns Deni's release-time source-integrity check into a trust signal the user can
    see: the brief asks that trusted information be traceable to credible sources and
    show when it was last updated. verify=true makes live network calls, so it is
    opt-in and used sparingly (e.g. a 'verify now' button), not on every load.
    """
    from .check_sources import summarize
    return summarize(country, verify=verify)


@app.get("/api/accountability/{scenario_key}")
def accountability(scenario_key: str, country: str = "ke") -> dict:
    """The accountability chain for one right: right -> law -> every public body with
    power over it -> the exact filing channel -> the document produced -> the source.

    Makes Deni's Transparency-track logic visible as a map of which institutions are
    accountable for a given right and how a citizen reaches each. Read from the data
    pack; no step is AI-generated.
    """
    from .data_pack import accountability_chain
    chain = accountability_chain(country, scenario_key)
    if not chain:
        raise HTTPException(status_code=404, detail=f"No right '{scenario_key}' in {country}")
    return chain


@app.get("/api/meta")
def meta(country: str = "ke") -> dict:
    """Country meta the UI needs to adapt labels: the licensing authority + examples."""
    from .data_pack import currency, licence_authority, load_pack
    la = licence_authority(country)
    langs = load_pack(country)["products"].get("_meta", {}).get(
        "languages", [{"code": "en", "label": "English"}])
    return {
        "country": country,
        "authority_short": la.get("authority_short", "the regulator"),
        "authority_name": la.get("authority_name", "the regulator"),
        "register_name": la.get("register_name", "the register"),
        "register_url": la.get("register_url"),
        "examples": la.get("examples", "e.g. a lender's name"),
        "currency": currency(country),
        "languages": langs,
    }


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
    country: str = "ke"


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


@app.post("/api/protect-letter")
def protect_letter(payload: RecourseIn) -> dict:
    """Draft a stop-contact letter sent DIRECT to the lender (Track 3: protection)."""
    return recourse_mod.protect_letter(payload.text, payload.lang, payload.country)


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
    country: str = "ke"


@app.post("/webhook/whatsapp")
def whatsapp_webhook(payload: WhatsAppIn) -> dict:
    """WhatsApp inbound webhook (JSON form, used by tests and generic providers)."""
    return {"reply": whatsapp.handle_message(payload.sender, payload.message, payload.country)}


@app.post("/webhook/twilio", response_class=PlainTextResponse)
async def twilio_whatsapp(From: str = Form(""), Body: str = Form(""),
                          country: str = "ke") -> str:
    """Twilio WhatsApp sandbox webhook: form-encoded From/Body in, TwiML XML out.

    Point the Twilio sandbox 'when a message comes in' webhook at this URL. Twilio
    delivers the reply we return in the <Message> element back to the user's WhatsApp.
    """
    reply = whatsapp.handle_message(From or "unknown", Body or "", country)
    safe = (reply.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{safe}</Message></Response>'


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
