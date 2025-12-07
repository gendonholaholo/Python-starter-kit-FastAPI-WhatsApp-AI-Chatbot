from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI WhatsApp AI"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # OpenAI
    OPENAI_API_KEY: str

    # WhatsApp
    WHATSAPP_TOKEN: str
    WHATSAPP_PHONE_NUMBER_ID: str
    WHATSAPP_VERIFY_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
