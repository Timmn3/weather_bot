from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def location_request_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отправить локацию", request_location=True)]],
        resize_keyboard=True
    )
