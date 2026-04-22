from datetime import datetime, timedelta
from app.core.config import settings
import base64
import json
import hmac
import hashlib
import bcrypt

def get_password_hash_ready(password: str) -> str:
    # 1. Hash with SHA-256
    sha256_hash = hashlib.sha256(password.encode("utf-8")).digest()
    # 2. Convert to Base64 to ensure it's a safe string under 72 chars
    return base64.b64encode(sha256_hash).decode("utf-8")

def hash_password(password: str) -> str:
    prepared_pw = get_password_hash_ready(password)
    hashed = bcrypt.hashpw(prepared_pw[:72].encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    prepared_pw = get_password_hash_ready(plain_password)
    try:
        return bcrypt.checkpw(
            prepared_pw[:72].encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except ValueError:
        # Treat invalid/oversized bcrypt inputs as non-matching credentials.
        return False

# JWT token generation
def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def create_access_token(data: dict) -> str:
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    payload = data.copy()
    payload.update({
        "exp": int((datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
        "iat": int(datetime.utcnow().timestamp())
    })

    header_encoded = base64url_encode(json.dumps(header).encode())
    payload_encoded = base64url_encode(json.dumps(payload).encode())

    signature_input = f"{header_encoded}.{payload_encoded}".encode()

    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        signature_input,
        hashlib.sha256
    ).digest()

    signature_encoded = base64url_encode(signature)

    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

def decode_token(token: str) -> dict:
    try:
        header_encoded, payload_encoded, signature = token.split(".")

        signature_input = f"{header_encoded}.{payload_encoded}".encode()

        expected_signature = hmac.new(
            settings.SECRET_KEY.encode(),
            signature_input,
            hashlib.sha256
        ).digest()

        expected_signature_encoded = base64url_encode(expected_signature)

        if not hmac.compare_digest(signature, expected_signature_encoded):
            raise Exception("Invalid signature")

        payload_bytes = base64url_decode(payload_encoded)
        payload = json.loads(payload_bytes)

        # Expiry check
        if payload.get("exp") < int(datetime.utcnow().timestamp()):
            raise Exception("Token expired")

        return payload

    except Exception:
        return None