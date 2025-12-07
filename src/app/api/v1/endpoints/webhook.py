import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from app.core.config import settings
from app.schemas.whatsapp import WhatsAppWebhook
from app.services.chat import chat_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(..., alias="hub.challenge"),
):
    """
    Verify webhook for WhatsApp.
    """
    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return int(challenge)

    logger.warning("Webhook verification failed")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def handle_webhook(payload: WhatsAppWebhook, background_tasks: BackgroundTasks):
    """
    Handle incoming WhatsApp messages.
    """
    logger.info(f"Received webhook payload: {payload.model_dump_json(indent=2)}")

    for entry in payload.entry:
        for change in entry.changes:
            if change.value.messages:
                for message in change.value.messages:
                    if message.type == "text" and message.text:
                        # Extract necessary info
                        wa_id = message.from_
                        name = (
                            change.value.contacts[0].profile["name"]
                            if change.value.contacts
                            else "Unknown"
                        )
                        body = message.text.body

                        # Process in background
                        background_tasks.add_task(
                            chat_service.process_message,
                            wa_id=wa_id,
                            name=name,
                            message_body=body,
                        )

    return {"status": "success"}
