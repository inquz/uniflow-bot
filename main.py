import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from db import (
    add_deadline,
    add_link,
    add_user,
    deactivate_deadline,
    deactivate_link,
    get_active_deadlines,
    get_active_links,
    get_user_by_telegram_id,
    get_users_count,
    init_db,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS_RAW = os.getenv("ADMIN_IDS", "")

ADMIN_IDS = {
    int(admin_id.strip())
    for admin_id in ADMIN_IDS_RAW.split(",")
    if admin_id.strip().isdigit()
}


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

router = Router()

WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def load_schedule() -> dict:
    path = Path("schedule.json")

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def format_schedule_for_day(days_offset: int = 0) -> str:
    schedule = load_schedule()

    target_date = datetime.now() + timedelta(days=days_offset)
    weekday_key = WEEKDAYS[target_date.weekday()]

    lessons = schedule.get(weekday_key, [])

    if not lessons:
        return "Пар нет или расписание пока не заполнено."

    lines = []

    for index, lesson in enumerate(lessons, start=1):
        time = lesson.get("time", "??:??")
        subject = lesson.get("subject", "Без названия")
        room = lesson.get("room", "не указана")
        teacher = lesson.get("teacher", "не указан")

        lines.append(
            f"{index}. {time} — {subject}\n"
            f"Аудитория: {room}\n"
            f"Преподаватель: {teacher}"
        )

    return "\n\n".join(lines)


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

    await message.answer(
        "Привет! UniFlow Bot запущен.\n\n"
        "Я сохранил тебя в базе данных.\n\n"
        "Команды:\n"
        "/today — расписание на сегодня\n"
        "/tomorrow — расписание на завтра\n"
        "/me — информация о тебе в базе\n"
        "/stats — статистика бота\n"
        "/help — помощь\n\n"
        f"Твой Telegram ID: {user.id}"
    )

@router.message(Command("me"))
async def me_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    db_user = get_user_by_telegram_id(user.id)

    if db_user is None:
        await message.answer("Тебя пока нет в базе. Напиши /start.")
        return

    await message.answer(
        "Ты есть в базе:\n\n"
        f"ID в базе: {db_user['id']}\n"
        f"Telegram ID: {db_user['telegram_id']}\n"
        f"Username: @{db_user['username']}\n"
        f"Имя: {db_user['first_name']}\n"
        f"Роль: {db_user['role']}\n"
        f"Создан: {db_user['created_at']}"
    )

@router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    users_count = get_users_count()

    await message.answer(
        "Статистика UniFlow Bot:\n\n"
        f"Пользователей в базе: {users_count}"
    )

@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
    "Команды UniFlow Bot:\n\n"
    "/today — пары на сегодня\n"
    "/tomorrow — пары на завтра\n"
    "/deadlines — ближайшие дедлайны\n"
    "/add_deadline — добавить дедлайн, только для админа\n"
    "/delete_deadline — удалить дедлайн, только для админа\n"
    "/links — полезные ссылки\n"
    "/add_link — добавить ссылку, только для админа\n"
    "/delete_link — удалить ссылку, только для админа\n"
    "/me — информация о тебе\n"
    "/stats — статистика\n"
    "/help — список команд"
)


@router.message(Command("today"))
async def today_handler(message: Message) -> None:
    text = format_schedule_for_day(days_offset=0)
    await message.answer(f"Пары на сегодня:\n\n{text}")


@router.message(Command("tomorrow"))
async def tomorrow_handler(message: Message) -> None:
    text = format_schedule_for_day(days_offset=1)
    await message.answer(f"Пары на завтра:\n\n{text}")

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

@router.message(Command("links"))
async def links_handler(message: Message) -> None:
    links = get_active_links()

    if not links:
        await message.answer("Ссылок пока нет.")
        return

    grouped_links: dict[str, list[dict]] = {}

    for link in links:
        subject = link["subject"]
        grouped_links.setdefault(subject, []).append(link)

    sections = []

    for subject, subject_links in grouped_links.items():
        lines = [f"{subject}:"]

        for link in subject_links:
            description = link["description"]

            if description:
                lines.append(
                    f"#{link['id']} {link['title']}\n"
                    f"{link['url']}\n"
                    f"{description}"
                )
            else:
                lines.append(
                    f"#{link['id']} {link['title']}\n"
                    f"{link['url']}"
                )

        sections.append("\n\n".join(lines))

    await message.answer("Полезные ссылки:\n\n" + "\n\n".join(sections))    

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

async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не найден. Проверь .env")

    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())