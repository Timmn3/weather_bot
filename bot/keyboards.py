# Клавиатуры: инлайн для единиц измерения, реплай для локации
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

def units_inline(selected: str = "metric") -> InlineKeyboardMarkup:
    """Инлайн-переключатель °C/°F с подсветкой выбранного."""
    def mark(val: str) -> str:
        return "✅" if val == selected else " "
    kb = [
        [
            InlineKeyboardButton(text=f"{mark('metric')} °C", callback_data="units:metric"),
            InlineKeyboardButton(text=f"{mark('imperial')} °F", callback_data="units:imperial"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def location_request_kb() -> ReplyKeyboardMarkup:
    """Кнопка для отправки геолокации."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отправить локацию", request_location=True)]],
        resize_keyboard=True
    )
