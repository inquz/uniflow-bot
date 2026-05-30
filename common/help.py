from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Команды UniFlow Bot:\n\n"
        "/today — пары на сегодня\n"
        "/tomorrow — пары на завтра\n"
        "/deadlines — ближайшие дедлайны\n"
        "/add_deadline — добавить дедлайн, только для admin/developer\n"
        "/delete_deadline — удалить дедлайн, только для admin/developer\n"
        "/links — полезные ссылки\n"
        "/add_link — добавить ссылку, только для admin/developer\n"
        "/delete_link — удалить ссылку, только для admin/developer\n"
        "/users — список пользователей, только для developer\n"
        "/set_role — изменить роль пользователя, только для developer\n"
        "/me — информация о тебе\n"
        "/stats — статистика\n"
        "/help — список команд"
    )
