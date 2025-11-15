"""Service to handle WhatsApp webhook processing logic."""
from app.schemas.whatsapp_webhook_schema import WhatsAppWebhookPayload
from app.utils.redis_connection import task_queue
from app.workers.whatsapp_worker import process_incoming_message

def process_whatsapp_message(payload: WhatsAppWebhookPayload):
    """
    All logic from what to do with WhatsApp Message webhook data
    """
    message = payload.entry[0].changes[0].value.messages[0]
    contact = payload.entry[0].changes[0].value.contacts[0]

    data = {
        "from": message.from_,
        "contact_name": contact.profile.get("name", ""),
        "message_body": message.text.body if message.text else None,
    }

    job = task_queue.enqueue(process_incoming_message, data)

    return {
        "status": "received",
        "job_id": job.get_id()
    }
