import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config import settings
from bot.handlers import setup_handlers

logging.basicConfig(level=logging.INFO)

async def main():
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN не задан. Укажи его в .env")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    setup_handlers(dp)

    logging.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

