from openai import AsyncOpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"  # Cost effective and fast
        self.system_prompt = "You are a helpful and friendly AI assistant on WhatsApp. Keep your responses concise and engaging."

    async def generate_response(
        self, user_message: str, context: list[dict] = None
    ) -> str:
        """
        Generate a response using OpenAI.

        Args:
            user_message: The current message from the user.
            context: List of previous messages in format [{"role": "user", "content": "..."}, ...]
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            messages.extend(context)

        messages.append({"role": "user", "content": user_message})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return (
                "Maaf, saya sedang mengalami gangguan saat ini. Mohon coba lagi nanti."
            )


openai_service = OpenAIService()
