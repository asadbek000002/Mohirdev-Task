from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from attorney.models import AttorneyEmail  # Admin orqali kiritilgan email manzillar


# Attorney'larga yangi lead haqida xabarnoma yuboradi
def send_email_to_attorneys(lead):
    subject = f"Yangi ariza: {lead.first_name} {lead.last_name}"
    from_email = settings.DEFAULT_FROM_EMAIL

    # Email jo'natiladigan attorney manzillari ro'yxati
    to = list(AttorneyEmail.objects.values_list("email", flat=True))

    context = {
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
    }
    # HTML va text shaklida email tarkibi
    html_content = render_to_string("emails/lead_created.html", context)
    text_content = f"Yangi ariza: {lead.first_name} {lead.last_name}, email: {lead.email}"

    # Email yaratish va jo'natish
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# Lead (foydalanuvchi) ga arizasi qabul qilingani haqida tasdiq xabari yuboradi
def send_confirmation_email_to_lead(lead, user_name=None):
    subject = "Arizangiz qabul qilindi"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [lead.email]

    context = {
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
        "user_name": user_name,
    }
    # HTML va text shaklida email tarkibi
    html_content = render_to_string("emails/lead_confirmation.html", context)
    text_content = "Rahmat, arizangiz qabul qilindi."

    # Email yaratish va jo'natish
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
