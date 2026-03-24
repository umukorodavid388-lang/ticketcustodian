from django.core.mail import send_mail
from django.conf import settings


def send_receipt_email(purchase):

    subject = "Ticket Payment Successful"

    message = f"""
Hello {purchase.first_name},

Your payment was successful.

Ticket: {purchase.ticket.name}
Reference: {purchase.payment_reference}

Thank you.
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [purchase.email],
        fail_silently=False,
    )
