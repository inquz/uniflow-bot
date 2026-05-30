import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

SCHEDULE_PATH = Path("schedule.json")
WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def load_schedule() -> dict[str, list[dict[str, Any]]]:
    if not SCHEDULE_PATH.exists():
        return {}

    with SCHEDULE_PATH.open("r", encoding="utf-8") as file:
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
