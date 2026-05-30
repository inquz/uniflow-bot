from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from schedule.service import format_schedule_for_day

router = Router()


@router.message(Command("tomorrow"))
async def tomorrow_handler(message: Message) -> None:
    text = format_schedule_for_day(days_offset=1)
    await message.answer(f"Пары на завтра:\n\n{text}")
