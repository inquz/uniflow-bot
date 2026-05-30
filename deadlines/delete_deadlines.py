from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from deadlines.repository import deactivate_deadline
from users.roles import is_admin

router = Router()


@router.message(Command("delete_deadline"))
async def delete_deadline_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    if not is_admin(user.id):
        await message.answer("У тебя нет прав на удаление дедлайнов.")
        return

    command_text = message.text or ""
    payload = command_text.replace("/delete_deadline", "", 1).strip()

    if not payload:
        await message.answer(
            "Формат:\n"
            "/delete_deadline ID\n\n"
            "Пример:\n"
            "/delete_deadline 3"
        )
        return

    if not payload.isdigit():
        await message.answer("ID должен быть числом.")
        return

    deadline_id = int(payload)

    deleted = deactivate_deadline(deadline_id)

    if not deleted:
        await message.answer(
            "Дедлайн не найден или уже удалён.\n\n"
            "Проверь ID через /deadlines."
        )
        return

    await message.answer(f"Дедлайн #{deadline_id} удалён.")
