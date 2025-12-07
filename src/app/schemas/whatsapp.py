from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class WhatsAppText(BaseModel):
    body: str

class WhatsAppMessage(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[WhatsAppText] = None

class WhatsAppContact(BaseModel):
    profile: Dict[str, str]
    wa_id: str

class WhatsAppMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class WhatsAppValue(BaseModel):
    messaging_product: str
    metadata: WhatsAppMetadata
    contacts: Optional[List[WhatsAppContact]] = None
    messages: Optional[List[WhatsAppMessage]] = None

class WhatsAppChange(BaseModel):
    value: WhatsAppValue
    field: str = "messages"

class WhatsAppEntry(BaseModel):
    id: str
    changes: List[WhatsAppChange]

class WhatsAppWebhook(BaseModel):
    object: str
    entry: List[WhatsAppEntry]
