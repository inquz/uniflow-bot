from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from links.repository import add_link
from users.roles import is_admin

router = Router()


@router.message(Command("add_link"))
async def add_link_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    if not is_admin(user.id):
        await message.answer("У тебя нет прав на добавление ссылок.")
        return

    command_text = message.text or ""
    payload = command_text.replace("/add_link", "", 1).strip()

    if not payload:
        await message.answer(
            "Формат:\n"
            "/add_link Предмет | Название | URL | Описание\n\n"
            "Описание можно не указывать.\n\n"
            "Пример:\n"
            "/add_link ООП | Методичка | https://example.com | Лабы и требования"
        )
        return

    parts = [part.strip() for part in payload.split("|")]

    if len(parts) not in (3, 4):
        await message.answer(
            "Неверный формат.\n\n"
            "Нужно так:\n"
            "/add_link Предмет | Название | URL | Описание\n\n"
            "Или без описания:\n"
            "/add_link Предмет | Название | URL"
        )
        return

    subject = parts[0]
    title = parts[1]
    url = parts[2]
    description = parts[3] if len(parts) == 4 else None

    if not url.startswith(("http://", "https://")):
        await message.answer("URL должен начинаться с http:// или https://")
        return

    add_link(
        subject=subject,
        title=title,
        url=url,
        description=description,
        created_by=user.id,
    )

    await message.answer(
        "Ссылка добавлена:\n\n"
        f"Предмет: {subject}\n"
        f"Название: {title}\n"
        f"URL: {url}"
    )
