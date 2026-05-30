import asyncio

from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN
from bot.routers import build_router
from database.schema import init_db


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не найден. Проверь .env")

    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(build_router())

    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
