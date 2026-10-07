import asyncio
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from .config import BOT_TOKEN, ADMIN_ID
from .handlers import router

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set.")
    if not ADMIN_ID:
        raise RuntimeError("ADMIN_ID is not set.")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
