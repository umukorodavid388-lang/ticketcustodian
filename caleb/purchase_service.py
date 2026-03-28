from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from datetime import timedelta
import uuid
from django.conf import settings
from .purchase_repo import *
from .seerbit_service import initialize_payment


def create_ticket_purchase(ticket, data):
    exchange_rates = {
        "NGN": Decimal("1"),
        "USD": Decimal("0.00071"),
        "GBP": Decimal("0.00053")
    }

    currency = data["currency"]
    price = Decimal(ticket.current_price())

    amount = (price * exchange_rates[currency]).quantize(Decimal("0.01"), ROUND_HALF_UP)

    payment_reference = f"TICKET-{ticket.id}-{uuid.uuid4().hex[:10]}"

    purchase_data = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "phone": data["phone"],
        "currency": currency,
        "country": data.get("country", ""),
        "state": data.get("state", ""),
        "how_did_you_hear": data.get("how_did_you_hear", ""),
        "ticket": ticket,
        "payment_reference": payment_reference,
        "expires_at": timezone.now() + timedelta(minutes=15)
    }

    purchase = create_purchase(purchase_data)

    payload = {
        "publicKey": settings.SEERBIT_PUBLIC_KEY,
        "amount": float(amount),
        "currency": currency,
        "country": "NG",
        "paymentReference": payment_reference,
        "email": data["email"],
        "fullName": f"{data['first_name']} {data['last_name']}",
        "mobileNumber": data["phone"],
        "callbackUrl": f"{settings.DOMAIN}/seerbit/callback/{purchase.id}/",
        "description": f"{ticket.name} Ticket Payment"
    }

    res = initialize_payment(payload)

    return res, purchase