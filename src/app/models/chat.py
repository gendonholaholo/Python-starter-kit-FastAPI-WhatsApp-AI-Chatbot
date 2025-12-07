from datetime import UTC, datetime

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wa_id: str = Field(index=True, unique=True)
    name: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    conversations: list["Conversation"] = Relationship(back_populates="user")


class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )  # To track last activity

    user: User = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str  # 'user' or 'system' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    conversation: Conversation = Relationship(back_populates="messages")
