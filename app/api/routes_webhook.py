"""Webhook endpoints for WhatsApp integration."""
import os
from fastapi import APIRouter, Request
from app.schemas.whatsapp_webhook_schema import WhatsAppWebhookPayload
from app.services.whatsapp_webhook_service import process_whatsapp_message

router = APIRouter()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

@router.get('/webhook')
def verify(request: Request):
    """
    Verify webhook endpoint for WhatsApp.

    request: FastAPI Request object containing query parameters.
    """
    mode = request.query_params.get("hub.mode")
    verify_token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and verify_token == VERIFY_TOKEN:
        return int(challenge)
    return "403 Forbidden"

@router.post('/webhook')
async def receive_webhook(payload: WhatsAppWebhookPayload):
    """
    Handle incoming webhook POST requests from WhatsApp.
    request: FastAPI Request object containing the JSON payload.
    """
    response = process_whatsapp_message(payload)

    return response
