from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from app.models.chat import User, Conversation, Message
from app.services.whatsapp import whatsapp_client
from app.services.ai import openai_service
from app.core.database import get_session
import logging

logger = logging.getLogger(__name__)


class ChatService:
    async def process_message(self, wa_id: str, name: str, message_body: str):
        """
        Process an incoming WhatsApp message.
        """
        # We need to manually manage the session here or inject it.
        # For simplicity in this background task nature, we'll create a new session.
        async for session in get_session():
            try:
                # 1. Get or Create User
                user = await self._get_or_create_user(session, wa_id, name)

                # 2. Get or Create Active Conversation
                conversation = await self._get_or_create_conversation(session, user.id)

                # 3. Save User Message
                await self._save_message(session, conversation.id, "user", message_body)

                # 4. Get History for AI context
                history = await self._get_conversation_history(session, conversation.id)

                # 5. Generate AI Response
                ai_response = await openai_service.generate_response(
                    message_body, history
                )

                # 6. Save Assistant Message
                await self._save_message(
                    session, conversation.id, "assistant", ai_response
                )

                # 7. Send WhatsApp Message
                await whatsapp_client.send_text_message(wa_id, ai_response)

            except Exception as e:
                logger.error(f"Error processing message from {wa_id}: {e}")
                # Optional: Send error message to user

    async def _get_or_create_user(
        self, session: AsyncSession, wa_id: str, name: str
    ) -> User:
        statement = select(User).where(User.wa_id == wa_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            user = User(wa_id=wa_id, name=name)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            logger.info(f"Created new user: {wa_id}")
        return user

    async def _get_or_create_conversation(
        self, session: AsyncSession, user_id: int
    ) -> Conversation:
        # Simplification: Just get the last updated conversation or create new.
        # Ideally we might have a timeout or explicit "new chat" logic.
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.updated_at))
        )
        result = await session.execute(statement)
        conversation = result.scalar_one_or_none()

        if not conversation:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)

        return conversation

    async def _save_message(
        self, session: AsyncSession, conversation_id: int, role: str, content: str
    ):
        message = Message(conversation_id=conversation_id, role=role, content=content)
        session.add(message)
        await session.commit()

    async def _get_conversation_history(
        self, session: AsyncSession, conversation_id: int, limit: int = 10
    ) -> list[dict]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .limit(limit)
        )
        result = await session.execute(statement)
        messages = result.scalars().all()

        return [{"role": msg.role, "content": msg.content} for msg in messages]


chat_service = ChatService()
