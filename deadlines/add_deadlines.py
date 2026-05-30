from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from deadlines.repository import add_deadline
from users.roles import is_admin

router = Router()


@router.message(Command("add_deadline"))
async def add_deadline_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    if not is_admin(user.id):
        await message.answer("У тебя нет прав на добавление дедлайнов.")
        return

    command_text = message.text or ""
    payload = command_text.replace("/add_deadline", "", 1).strip()

    if not payload:
        await message.answer(
            "Формат:\n"
            "/add_deadline Предмет | Название | YYYY-MM-DD HH:MM\n\n"
            "Пример:\n"
            "/add_deadline ООП | Лаба №3 | 2026-06-01 23:59"
        )
        return

    parts = [part.strip() for part in payload.split("|")]

    if len(parts) != 3:
        await message.answer(
            "Неверный формат.\n\n"
            "Нужно так:\n"
            "/add_deadline Предмет | Название | YYYY-MM-DD HH:MM"
        )
        return

    subject, title, due_at = parts

    try:
        datetime.strptime(due_at, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer(
            "Дата указана неверно.\n\n"
            "Нужный формат:\n"
            "YYYY-MM-DD HH:MM\n\n"
            "Пример:\n"
            "2026-06-01 23:59"
        )
        return

    add_deadline(
        subject=subject,
        title=title,
        due_at=due_at,
        created_by=user.id,
    )

    await message.answer(
        "Дедлайн добавлен:\n\n"
        f"Предмет: {subject}\n"
        f"Задача: {title}\n"
        f"Дата: {due_at}"
    )
