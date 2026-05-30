from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from users.repository import get_users
from users.roles import is_developer

router = Router()


@router.message(Command("users"))
async def users_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    if not is_developer(user.id):
        await message.answer("У тебя нет прав на просмотр пользователей.")
        return

    users = get_users()

    if not users:
        await message.answer("Пользователей пока нет.")
        return

    lines = []

    for db_user in users:
        username = f"@{db_user['username']}" if db_user["username"] else "нет"
        first_name = db_user["first_name"] or "нет"

        lines.append(
            f"ID в базе: {db_user['id']}\n"
            f"Telegram ID: {db_user['telegram_id']}\n"
            f"Username: {username}\n"
            f"Имя: {first_name}\n"
            f"Роль: {db_user['role']}"
        )

    await message.answer("Пользователи:\n\n" + "\n\n".join(lines))
