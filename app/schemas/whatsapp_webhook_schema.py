from typing import List, Optional
from pydantic import BaseModel, Field

class TextMessage(BaseModel):
    body: str

class Message(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[TextMessage] = None

class Contact(BaseModel):
    profile: dict
    wa_id: str

class Value(BaseModel):
    messaging_product: str
    metadata: dict
    contacts: List[Contact]
    messages: List[Message]

class Changes(BaseModel):
    value: Value

class Entry(BaseModel):
    id: str
    changes: List[Changes]

class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[Entry]

    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }
