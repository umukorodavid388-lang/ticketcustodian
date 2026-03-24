from django.db import models
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta

class Ticket(models.Model):

    TICKET_TYPES = (
        ('regular', 'Regular'),
        ('vip', 'VIP'),
        ('vvip', 'VVIP'),
    )

    name = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPES)

    # Regular ticket pricing
    early_bird_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    late_bird_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    early_start = models.DateTimeField(null=True, blank=True)
    early_end = models.DateTimeField(null=True, blank=True)

    late_start = models.DateTimeField(null=True, blank=True)
    late_end = models.DateTimeField(null=True, blank=True)

    # VIP & VVIP fixed price
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    price_currency = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('15000.00'))  # Default exchange rate for Naira

    created_at = models.DateTimeField(auto_now_add=True)

    def current_price(self):
        now = timezone.now()

        if self.ticket_type == 'regular':
            if self.early_start and self.early_end and self.early_bird_price is not None:
                if self.early_start <= now <= self.early_end:
                    return Decimal(self.early_bird_price)

            if self.late_start and self.late_end and self.late_bird_price is not None:
                if self.late_start <= now <= self.late_end:
                    return Decimal(self.late_bird_price)

            return None

        # VIP / VVIP
        if self.price is not None:
            return Decimal(self.price)
        if self.price_currency is not None:
            return Decimal(self.price_currency)

        return None


    def phase(self):
        now = timezone.now()

        if self.ticket_type == 'regular':
            if self.early_start and self.early_end:
                if self.early_start <= now <= self.early_end:
                    return "Early Bird"

            if self.late_start and self.late_end:
                if self.late_start <= now <= self.late_end:
                    return "Late Bird"

            return "Closed"

        return self.get_ticket_type_display()

    def is_available(self):
        return self.current_price() is not None

    def __str__(self):
        return f"{self.name} - {self.get_ticket_type_display()}"


class BankAccount(models.Model):

    CURRENCY_CHOICES = (
        ("NGN", "Naira"),
        ("USD", "Dollar"),
        ("GBP", "Pounds"),
    )

    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.currency} - {self.bank_name} - {self.account_name}"



class TicketPurchase(models.Model):

    HEAR_CHOICES = (
        ("social-media", "Social Media"),
        ("friend", "Friend"),
        ("advertisement", "Advertisement"),
    )

    CURRENCY_CHOICES = (
        ("NGN", "Naira"),
        ("USD", "Dollar"),
        ("GBP", "Pounds"),
    )

    # Buyer info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Location
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    # Payment
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)

    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Ticket
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Survey
    how_did_you_hear = models.CharField(
        max_length=50,
        choices=HEAR_CHOICES
    )

    # Payment status
    is_paid = models.BooleanField(default=False)

    # Reference
    payment_reference = models.CharField(max_length=200)

    is_paid = models.BooleanField(default=False)

    payment_proof = models.ImageField(
        upload_to="payment_proofs/",
        null=True,
        blank=True
    )

    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def set_expiry(self):
        self.expires_at = timezone.now() + timedelta(minutes=5)
        self.save()

    def is_expired(self):
        return timezone.now() > self.expires_at

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.ticket}"


