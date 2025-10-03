import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    weather_api_key: str = os.getenv("WEATHER_API_KEY", "")
    default_units: str = os.getenv("DEFAULT_UNITS", "metric")  # metric | imperial
    openweather_lang: str = os.getenv("OPENWEATHER_LANG", "ru")
    cache_ttl_seconds: int = 300  # 5 минут

settings = Settings()
