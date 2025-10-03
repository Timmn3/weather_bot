import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

@dataclass(frozen=True)
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    weather_api_key: str = os.getenv("WEATHER_API_KEY", "")
    default_units: str = os.getenv("DEFAULT_UNITS", "metric")
    cache_ttl_seconds: int = 300

settings = Settings()
