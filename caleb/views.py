from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .purchase_service import create_ticket_purchase
from .seerbit_service import verify_payment
from .purchase_repo import *
from .email import send_receipt_email
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from .utils import generate_receipt

# =========================
# BASIC VIEWS
# =========================
def index(request):
    return render(request, 'index.html')


def safe_decimal(value):
    try:
        return Decimal(value)
    except (TypeError, InvalidOperation):
        return Decimal('0.00')


# =========================
# TICKET LIST
# =========================
def ticket_list(request):
    NAIRA_TO_DOLLAR = Decimal('1') / Decimal('1400')
    NAIRA_TO_POUND = Decimal('1') / Decimal('1900')

    tickets = Ticket.objects.all()
    active_tickets = []

    for ticket in tickets:
        price = safe_decimal(ticket.current_price())

        active_tickets.append({
            'id': ticket.id,
            'name': ticket.name,
            'phase_label': ticket.phase(),
            'price_naira': price,
            'price_dollar': (price * NAIRA_TO_DOLLAR).quantize(Decimal('0.01'), ROUND_HALF_UP),
            'price_pound': (price * NAIRA_TO_POUND).quantize(Decimal('0.01'), ROUND_HALF_UP),
            'is_active': ticket.is_available(),
        })

    return render(request, 'indexs.html', {'tickets': active_tickets})


# =========================
# BANK DETAILS
# =========================
def get_account_details(request):
    currency = request.GET.get("currency")
    account = BankAccount.objects.filter(currency=currency).first()
    if account:
        return JsonResponse({
            "account_number": account.account_number,
            "bank_name": account.bank_name,
            "account_name": account.account_name,
        })
    return JsonResponse({
        "account_number": "",
        "bank_name": "",
        "account_name": "",
    })








def create_purchase_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "currency": request.POST.get("currency"),
        }

        res, purchase = create_ticket_purchase(ticket, data)

        if res.get("status") == "SUCCESS":
            return redirect(res["data"]["payments"]["redirectLink"])

        return render(request, "payment_error.html", {"message": res})


def seerbit_callback(request, purchase_id):
    reference = request.GET.get("paymentReference")

    purchase = get_purchase_by_id_and_reference(purchase_id, reference)

    if not purchase:
        return render(request, "payment_error.html")

    res = verify_payment(reference)

    if res.get("status") == "SUCCESS" and res["data"]["payments"]["status"] == "SUCCESS":
        mark_as_paid(purchase)
        send_receipt_email(purchase)

        return render(request, "payment_success.html", {"purchase": purchase})

    return render(request, "payment_error.html")