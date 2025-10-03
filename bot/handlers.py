from aiogram import Router, F, Dispatcher
from aiogram.types import Message, ContentType
from aiogram.filters import Command
import re

from config import settings
from weather.api_client import OpenWeatherClient
from weather.cache import WeatherCache, UserUnitsStore
from weather.formatting import format_weather_report
from bot.keyboards import location_request_kb

router = Router()

# in-memory хранилища
cache = WeatherCache(ttl_seconds=settings.cache_ttl_seconds)
user_units = UserUnitsStore(default_units=settings.default_units)
client = OpenWeatherClient(api_key=settings.weather_api_key, lang=settings.openweather_lang)

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    # ВАЖНО: экранируем угловые скобки из-за HTML parse_mode
    text = (
        "Привет! Я бот погоды.\n\n"
        "Команды:\n"
        "/weather &lt;город&gt; — пример: <code>/weather Berlin</code>\n"
        "/celsius — вывод в °C\n"
        "/fahrenheit — вывод в °F\n\n"
        "Можно отправить локацию кнопкой ниже или ввести координаты:\n"
        "<code>55.7558, 37.6176</code> (Москва)"
    )
    await message.answer(text, reply_markup=location_request_kb())

@router.message(Command("celsius"))
async def cmd_celsius(message: Message) -> None:
    user_units.set_units(message.from_user.id, "metric")
    await message.answer("Ок, теперь показываю в °C.")

@router.message(Command("fahrenheit"))
async def cmd_fahrenheit(message: Message) -> None:
    user_units.set_units(message.from_user.id, "imperial")
    await message.answer("Готово, теперь показываю в °F.")

@router.message(Command("weather"))
async def cmd_weather(message: Message) -> None:
    # ожидаем /weather <город>
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await message.answer(
            "Укажи город: например, <code>/weather Paris</code> или <code>/weather Tokyo</code>."
        )
        return

    city = parts[1].strip()
    units = user_units.get_units(message.from_user.id)
    cache_key = ("city", city.lower(), units)

    cached = cache.get(cache_key)
    if cached:
        await message.answer(format_weather_report(cached, units))
        return

    try:
        report = await client.get_by_city(city=city, units=units)
    except Exception:
        await message.answer(
            "Не удалось получить погоду 😔\n"
            "Проверь название города.\n"
            "Примеры: <code>/weather London</code>, <code>/weather New York</code>."
        )
        return

    cache.set(cache_key, report)
    await message.answer(format_weather_report(report, units))

@router.message(F.content_type == ContentType.LOCATION)
async def on_location(message: Message) -> None:
    if not message.location:
        await message.answer(
            "Не удалось прочитать координаты 😔\n\n"
            "Попробуй снова отправить локацию через кнопку.\n"
            "Или введи координаты вручную в формате:\n"
            "<code>55.7558, 37.6176</code> (Москва)\n"
            "<code>40.7128, -74.0060</code> (Нью-Йорк)"
        )
        return

    lat, lon = message.location.latitude, message.location.longitude
    units = user_units.get_units(message.from_user.id)
    cache_key = ("coords", round(lat, 3), round(lon, 3), units)

    cached = cache.get(cache_key)
    if cached:
        await message.answer(format_weather_report(cached, units))
        return

    try:
        report = await client.get_by_coords(lat=lat, lon=lon, units=units)
    except Exception:
        await message.answer(
            "Не удалось получить погоду по координатам 😔\n\n"
            "Попробуй снова отправить локацию или укажи город:\n"
            "<code>/weather Paris</code>"
        )
        return

    cache.set(cache_key, report)
    await message.answer(format_weather_report(report, units))

# ручной ввод координат: "55.7558, 37.6176"
@router.message(F.text)
async def manual_coords(message: Message) -> None:
    text = message.text.strip()

    # Проверяем шаблон "lat, lon"
    if not re.match(r"^\s*-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?\s*$", text):
        # Сообщение пользователю, если формат некорректный
        if any(ch.isdigit() for ch in text):  # похоже на координаты, но не валидно
            await message.answer(
                "Некорректный формат координат.\n"
                "Пример правильного ввода:\n"
                "<code>55.7558, 37.6176</code> (Москва)\n"
                "<code>40.7128, -74.0060</code> (Нью-Йорк)"
            )
        return

    try:
        lat_str, lon_str = re.split(r",\s*", text)
        lat, lon = float(lat_str), float(lon_str)
    except Exception:
        await message.answer(
            "Не удалось обработать координаты.\n"
            "Пример: <code>55.7558, 37.6176</code>"
        )
        return

    units = user_units.get_units(message.from_user.id)
    cache_key = ("coords", round(lat, 3), round(lon, 3), units)

    cached = cache.get(cache_key)
    if cached:
        await message.answer(format_weather_report(cached, units))
        return

    try:
        report = await client.get_by_coords(lat=lat, lon=lon, units=units)
    except Exception:
        await message.answer(
            "Не удалось получить погоду по координатам.\n"
            "Попробуй снова или задай город через /weather <город>."
        )
        return

    cache.set(cache_key, report)
    await message.answer(format_weather_report(report, units))

def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)
