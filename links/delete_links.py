from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from links.repository import deactivate_link
from users.roles import is_admin

router = Router()


@router.message(Command("delete_link"))
async def delete_link_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    if not is_admin(user.id):
        await message.answer("У тебя нет прав на удаление ссылок.")
        return

    command_text = message.text or ""
    payload = command_text.replace("/delete_link", "", 1).strip()

    if not payload:
        await message.answer(
            "Формат:\n"
            "/delete_link ID\n\n"
            "Пример:\n"
            "/delete_link 2"
        )
        return

    if not payload.isdigit():
        await message.answer("ID должен быть числом.")
        return

    link_id = int(payload)

    deleted = deactivate_link(link_id)

    if not deleted:
        await message.answer(
            "Ссылка не найдена или уже удалена.\n\n"
            "Проверь ID через /links."
        )
        return

    await message.answer(f"Ссылка #{link_id} удалена.")
