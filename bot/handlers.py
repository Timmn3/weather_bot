from aiogram import Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import re
from config import settings
from weather.api_client import OpenWeatherClient
from weather.cache import WeatherCache, UserUnitsStore
from weather.formatting import format_weather_report
from bot.keyboards import units_inline, location_request_kb
from bot.states import WeatherStates

router = Router()

cache = WeatherCache(ttl_seconds=settings.cache_ttl_seconds)
user_units = UserUnitsStore(default_units=settings.default_units)
client = OpenWeatherClient(api_key=settings.weather_api_key, lang=settings.openweather_lang)

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    text = (
        "Привет! Я бот прогноза погоды.\n\n"
        "Можешь отправить локацию или ввести название города.\n"
        "Например: <code>Moscow</code> или <code>New York</code>.\n\n"
        "Выбери единицы измерения ниже:"
    )
    await message.answer(text, reply_markup=location_request_kb())
    await message.answer("Выбор единиц:", reply_markup=units_inline())

@router.callback_query(F.data.startswith("units:"))
async def units_change(cb: CallbackQuery) -> None:
    val = cb.data.split(":", 1)[1]
    user_units.set_units(cb.from_user.id, val)
    await cb.message.edit_reply_markup(reply_markup=units_inline(val))
    await cb.answer("Настройки сохранены.")

@router.message(Command("weather"))
async def cmd_weather(message: Message, state: FSMContext) -> None:
    await message.answer("Введи название города (например: <code>Berlin</code>):")
    await state.set_state(WeatherStates.waiting_for_city)

@router.message(WeatherStates.waiting_for_city)
async def get_city(message: Message, state: FSMContext) -> None:
    city = message.text.strip()
    units = user_units.get_units(message.from_user.id)
    cache_key = ("city", city.lower(), units)

    cached = cache.get(cache_key)
    if cached:
        await message.answer(format_weather_report(cached, units))
        await state.clear()
        return

    try:
        report = await client.get_by_city(city=city, units=units)
    except Exception:
        await message.answer(
            "Не удалось получить погоду 😔\n\n"
            "Проверь правильность названия.\n"
            "Примеры: <code>Paris</code>, <code>Tokyo</code>."
        )
        await state.clear()
        return

    cache.set(cache_key, report)
    await message.answer(format_weather_report(report, units))
    await state.clear()

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
            "Попробуй снова отправить локацию или задай город командой /weather.\n"
            "Также можно ввести координаты вручную, пример:\n"
            "<code>48.8566, 2.3522</code> (Париж)"
        )
        return

    cache.set(cache_key, report)
    await message.answer(format_weather_report(report, units))

@router.message(F.text.regexp(r"^-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?$"))
async def manual_coords(message: Message) -> None:
    """Обработка ручного ввода координат в формате 'lat, lon'."""
    try:
        lat_str, lon_str = re.split(r",\s*", message.text.strip())
        lat, lon = float(lat_str), float(lon_str)
    except Exception:
        await message.answer(
            "Не удалось разобрать координаты 😔\n"
            "Пример правильного ввода:\n"
            "<code>55.7558, 37.6176</code> (Москва)\n"
            "<code>40.7128, -74.0060</code> (Нью-Йорк)"
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
            "Не удалось получить погоду по координатам 😔\n"
            "Попробуй ещё раз или отправь локацию кнопкой."
        )
        return

    cache.set(cache_key, report)
    await message.answer(format_weather_report(report, units))



def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)
