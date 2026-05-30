from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from users.repository import add_user, get_user_by_telegram_id
from users.roles import sync_env_role

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    add_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )

    sync_env_role(user.id)

    db_user = get_user_by_telegram_id(user.id)
    role = db_user["role"] if db_user is not None else "student"

    await message.answer(
        "Привет! UniFlow Bot запущен.\n\n"
        "Я сохранил тебя в базе данных.\n\n"
        "Команды:\n"
        "/today — расписание на сегодня\n"
        "/tomorrow — расписание на завтра\n"
        "/deadlines — ближайшие дедлайны\n"
        "/links — полезные ссылки\n"
        "/me — информация о тебе в базе\n"
        "/stats — статистика бота\n"
        "/help — помощь\n\n"
        f"Твой Telegram ID: {user.id}\n"
        f"Твоя роль: {role}"
    )
