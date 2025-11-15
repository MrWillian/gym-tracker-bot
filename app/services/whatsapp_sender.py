"""Service to send WhatsApp messages via WhatsApp Business API."""
import os
import requests

WHATSAPP_API_URL = "https://graph.facebook.com/v17.0"
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

def send_whatsapp_message(to_number: str, message: str):
    """Send a WhatsApp message using the WhatsApp Business API."""
    url = f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages"
    headers = {
      "Authorization": f"Bearer {ACCESS_TOKEN}",
      "Content-Type": "application/json"
    }

    payload = {
      "messaging_product": "whatsapp",
      "to": to_number,
      "type": "text",
      "text": {
        "body": message
      }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    return response.json()
