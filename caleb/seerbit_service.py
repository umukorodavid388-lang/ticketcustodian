import requests
import json
import base64
import hashlib
from Crypto.Cipher import AES
from django.conf import settings


# =========================
# 🔐 ENCRYPTION
# =========================
def pad(data):
    block_size = 16
    pad_len = block_size - (len(data) % block_size)
    return data + chr(pad_len) * pad_len


def encrypt_payload(payload, key):
    raw = json.dumps(payload)
    hashed_key = hashlib.sha256(key.encode()).digest()
    iv = hashed_key[:16]

    cipher = AES.new(hashed_key, AES.MODE_CBC, iv)
    padded = pad(raw)

    encrypted = cipher.encrypt(padded.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


# =========================
# 🔐 GET TOKEN
# =========================
def get_encrypted_key():
    url = "https://seerbitapi.com/api/v2/encrypt/keys"
    payload = {"key": settings.SEERBIT_SECRET_KEY}

    response = requests.post(url, json=payload)
    data = response.json()

    return data.get("data", {}).get("EncryptedSecKey", {}).get("encryptedKey")


# =========================
# 💳 INITIALIZE PAYMENT
# =========================
def initialize_payment(payload):
    key = get_encrypted_key()
    encrypted_data = encrypt_payload(payload, key)

    response = requests.post(
        "https://seerbitapi.com/api/v2/payments",
        json={"encrypted_data": encrypted_data},
        headers={"Content-Type": "application/json"}
    )

    

    return response.json()


# =========================
# ✔️ VERIFY PAYMENT
# =========================
def verify_payment(reference):
    url = f"https://seerbitapi.com/api/v2/payments/query/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.SEERBIT_PUBLIC_KEY}"
    }

    response = requests.get(url, headers=headers)
    return response.json()