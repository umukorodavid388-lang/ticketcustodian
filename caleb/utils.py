from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_receipt(purchase):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Payment Receipt", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Name: {purchase.first_name} {purchase.last_name}", styles["Normal"]))
    elements.append(Paragraph(f"Email: {purchase.email}", styles["Normal"]))
    elements.append(Paragraph(f"Ticket: {purchase.ticket}", styles["Normal"]))
    elements.append(Paragraph(f"Amount: {purchase.ticket.price} {purchase.currency}", styles["Normal"]))
    elements.append(Paragraph(f"Reference: {purchase.payment_reference}", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer



from django.core.mail import EmailMessage

def send_receipt_email(purchase):
    pdf_buffer = generate_receipt(purchase)

    # Send to buyer
    email_buyer = EmailMessage(
        subject="Your Ticket Payment Receipt",
        body=f"Hello {purchase.first_name},\n\nYour payment has been confirmed. Receipt attached.",
        to=[purchase.email]
    )
    email_buyer.attach("receipt.pdf", pdf_buffer.read(), "application/pdf")
    email_buyer.send()

    # Send copy to admin
    email_admin = EmailMessage(
        subject="New Ticket Payment",
        body=f"{purchase.first_name} {purchase.last_name} has paid for ticket {purchase.ticket}.",
        to=["youremail@gmail.com"]
    )
    email_admin.send()
