from celery import shared_task
import logging

from attorney.models import EmailErrorLog
from intake.models import Lead
from intake.utils import send_email_to_attorneys, send_confirmation_email_to_lead

logger = logging.getLogger(__name__)


# Attorney'larga yangi lead haqida email yuboradigan Celery task
@shared_task
def attorney_email_task(lead_id):
    try:
        lead = Lead.objects.get(id=lead_id)
        send_email_to_attorneys(lead)

        logger.info(f"Email successfully sent to {lead.email}")
    except Lead.DoesNotExist:
        logger.error(f"Lead with id {lead_id} not found")
        EmailErrorLog.objects.create(
            lead_id=lead_id,
            email="N/A",
            error_message="Lead not found"
        )
    except Exception as e:
        logger.error(f"Email sending failed for lead_id={lead_id}, error={str(e)}")
        EmailErrorLog.objects.create(
            lead_id=lead.id,
            email=lead.email,
            error_message=str(e)
        )


# Lead foydalanuvchisiga arizasi qabul qilinganini tasdiqlovchi email yuboradigan task
@shared_task
def lead_email_task(lead_id, user_name=None):
    try:
        lead = Lead.objects.get(id=lead_id)
        send_confirmation_email_to_lead(lead, user_name)

        logger.info(f"Email successfully sent to {lead.email}")
    except Lead.DoesNotExist:
        logger.error(f"Lead with id {lead_id} not found")
        EmailErrorLog.objects.create(
            lead_id=lead_id,
            email="N/A",
            error_message="Lead not found"
        )
    except Exception as e:
        logger.error(f"Email sending failed for lead_id={lead_id}, error={str(e)}")
        EmailErrorLog.objects.create(
            lead_id=lead.id,
            email=lead.email,
            error_message=str(e)
        )
