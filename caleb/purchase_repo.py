from .models import TicketPurchase


def create_purchase(data):
    return TicketPurchase.objects.create(**data)


def get_purchase_by_reference(reference):
    return TicketPurchase.objects.filter(payment_reference=reference).first()


def get_purchase_by_id_and_reference(purchase_id, reference):
    return TicketPurchase.objects.filter(id=purchase_id, payment_reference=reference).first()


def mark_as_paid(purchase):
    purchase.is_paid = True
    purchase.save()
    return purchase