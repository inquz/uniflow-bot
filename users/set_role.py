from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from users.repository import set_user_role
from users.roles import is_developer

router = Router()


@router.message(Command("set_role"))
async def set_role_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    if not is_developer(user.id):
        await message.answer("У тебя нет прав на изменение ролей.")
        return

    command_text = message.text or ""
    payload = command_text.replace("/set_role", "", 1).strip()

    if not payload:
        await message.answer(
            "Формат:\n"
            "/set_role Telegram_ID role\n\n"
            "Доступные роли:\n"
            "student, admin, developer\n\n"
            "Пример:\n"
            "/set_role 123456789 admin"
        )
        return

    parts = payload.split()

    if len(parts) != 2:
        await message.answer(
            "Неверный формат.\n\n"
            "Нужно так:\n"
            "/set_role Telegram_ID role"
        )
        return

    telegram_id_raw, role = parts

    if not telegram_id_raw.isdigit():
        await message.answer("Telegram ID должен быть числом.")
        return

    if role not in {"student", "admin", "developer"}:
        await message.answer(
            "Такой роли нет.\n\n"
            "Доступные роли:\n"
            "student, admin, developer"
        )
        return

    telegram_id = int(telegram_id_raw)
    updated = set_user_role(telegram_id, role)

    if not updated:
        await message.answer(
            "Пользователь не найден в базе.\n\n"
            "Он должен сначала написать /start боту."
        )
        return

    await message.answer(
        "Роль изменена:\n\n"
        f"Telegram ID: {telegram_id}\n"
        f"Новая роль: {role}"
    )
