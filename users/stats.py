from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from users.repository import get_users_count

router = Router()


@router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    users_count = get_users_count()

    await message.answer(
        "Статистика UniFlow Bot:\n\n"
        f"Пользователей в базе: {users_count}"
    )
