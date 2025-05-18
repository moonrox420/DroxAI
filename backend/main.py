from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, validator
from decouple import config
import stripe
from cryptography.fernet import Fernet
import logging
import sqlite3
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Initialize FastAPI app
app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.get('/health')async def health_check(): return {status: OK}, 200

# Configure CORS
ALLOWED_ORIGINS = (
    ["https://droxai.io"] if config("ENV", default="development") == "production"
    else ["https://droxai.io", "http://localhost:3000"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)

# Load configurations
stripe.api_key = config("STRIPE_API_KEY")
WEBHOOK_SECRET = config("WEBHOOK_SECRET")
cipher = Fernet(config("FERNET_KEY"))
logging.basicConfig(filename="app.log", level=logging.INFO)

# Price IDs from environment variables
PRICE_IDS = {
    "glacier": {
        "onboarding": config("GLACIER_ONBOARDING_PRICE_ID"),
        "subscription": config("GLACIER_SUBSCRIPTION_PRICE_ID"),
    },
    "hollow": {
        "onboarding": config("HOLLOW_ONBOARDING_PRICE_ID"),
        "subscription": config("HOLLOW_SUBSCRIPTION_PRICE_ID"),
    },
    "forge": {
        "onboarding": config("FORGE_ONBOARDING_PRICE_ID"),
        "subscription": config("FORGE_SUBSCRIPTION_PRICE_ID"),
    },
    "brahma": {
        "onboarding": config("BRAHMA_ONBOARDING_PRICE_ID"),
        "subscription": config("BRAHMA_SUBSCRIPTION_PRICE_ID"),
    },
}

# Authentication
api_key_header = APIKeyHeader(name="X-API-Key")
async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != config("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

# Encrypted logging
def log_encrypted(message: str):
    """Encrypt and log messages."""
    try:
        encrypted_message = cipher.encrypt(message.encode())
        logging.info(encrypted_message)
    except Exception as e:
        logging.error(f"Logging error: {str(e)}")

# Pydantic model for checkout request
class CheckoutRequest(BaseModel):
    tier: str

    @validator("tier")
    def validate_tier(cls, v):
        valid_tiers = ["glacier", "hollow", "forge", "brahma"]
        if v not in valid_tiers:
            raise ValueError(f"Tier must be one of {valid_tiers}")
        return v

# Webhook idempotency
def is_event_processed(event_id: str) -> bool:
    """Check if webhook event has been processed."""
    try:
        conn = sqlite3.connect("webhooks.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS webhooks (event_id TEXT PRIMARY KEY)")
        cursor.execute("SELECT event_id FROM webhooks WHERE event_id = ?", (event_id,))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO webhooks (event_id) VALUES (?)", (event_id,))
            conn.commit()
            conn.close()
            return False
        conn.close()
        return True
    except sqlite3.Error as e:
        log_encrypted(f"Database error: {str(e)}")
        return False

@app.post("/create-checkout-session")
@limiter.limit("5/minute")
async def create_checkout_session(request: CheckoutRequest, api_key: str = Depends(verify_api_key)):
    """Create a Stripe checkout session for the specified tier."""
    try:
        if request.tier not in PRICE_IDS:
            log_encrypted(f"Invalid tier requested: {request.tier}")
            raise HTTPException(status_code=400, detail="Invalid tier")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {"price": PRICE_IDS[request.tier]["onboarding"], "quantity": 1},
                {"price": PRICE_IDS[request.tier]["subscription"], "quantity": 1},
            ],
            mode="subscription",
            success_url="https://droxai.io/success",
            cancel_url="https://droxai.io/cancel",
            metadata={"tier": request.tier},
        )
        log_enc
