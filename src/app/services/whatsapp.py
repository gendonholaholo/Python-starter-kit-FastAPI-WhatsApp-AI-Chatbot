import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class WhatsAppClient:
    def __init__(self):
        self.api_url = f"https://graph.facebook.com/v21.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        self.headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
            "Content-Type": "application/json",
        }

    async def send_text_message(self, to: str, body: str):
        """Send a text message to a WhatsApp user."""
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body},
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url, headers=self.headers, json=payload, timeout=10.0
                )
                response.raise_for_status()
                logger.info(f"Message sent to {to}: {response.json()}")
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Failed to send message: {e}")
                if isinstance(e, httpx.HTTPStatusError):
                    logger.error(f"Response content: {e.response.text}")
                raise


whatsapp_client = WhatsAppClient()
