from pydantic import BaseModel, Field


class WhatsAppText(BaseModel):
    body: str


class WhatsAppMessage(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: str
    text: WhatsAppText | None = None


class WhatsAppContact(BaseModel):
    profile: dict[str, str]
    wa_id: str


class WhatsAppMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class WhatsAppValue(BaseModel):
    messaging_product: str
    metadata: WhatsAppMetadata
    contacts: list[WhatsAppContact] | None = None
    messages: list[WhatsAppMessage] | None = None


class WhatsAppChange(BaseModel):
    value: WhatsAppValue
    field: str = "messages"


class WhatsAppEntry(BaseModel):
    id: str
    changes: list[WhatsAppChange]


class WhatsAppWebhook(BaseModel):
    object: str
    entry: list[WhatsAppEntry]
