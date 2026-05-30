from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from deadlines.repository import get_active_deadlines

router = Router()


@router.message(Command("deadlines"))
async def deadlines_handler(message: Message) -> None:
    deadlines = get_active_deadlines()

    if not deadlines:
        await message.answer("Дедлайнов пока нет.")
        return

    lines = []

    for index, deadline in enumerate(deadlines, start=1):
        lines.append(
            f"{index}. #{deadline['id']} {deadline['subject']} — {deadline['title']}\n"
            f"До: {deadline['due_at']}"
        )

    await message.answer("Ближайшие дедлайны:\n\n" + "\n\n".join(lines))
