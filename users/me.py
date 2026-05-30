from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from users.repository import get_user_by_telegram_id

router = Router()


@router.message(Command("me"))
async def me_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    db_user = get_user_by_telegram_id(user.id)

    if db_user is None:
        await message.answer("Тебя пока нет в базе. Напиши /start.")
        return

    username = f"@{db_user['username']}" if db_user["username"] else "не указан"
    first_name = db_user["first_name"] if db_user["first_name"] else "не указано"

    await message.answer(
        "Ты есть в базе:\n\n"
        f"ID в базе: {db_user['id']}\n"
        f"Telegram ID: {db_user['telegram_id']}\n"
        f"Username: {username}\n"
        f"Имя: {first_name}\n"
        f"Роль: {db_user['role']}\n"
        f"Создан: {db_user['created_at']}"
    )
