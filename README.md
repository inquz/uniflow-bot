# UniFlow Bot

Telegram-бот для учебной группы: расписание, дедлайны и полезные ссылки.

## Возможности

- `/start` — регистрация пользователя
- `/today` — расписание на сегодня
- `/tomorrow` — расписание на завтра
- `/deadlines` — список дедлайнов
- `/add_deadline` — добавить дедлайн, только для admin/developer
- `/delete_deadline` — удалить дедлайн, только для admin/developer
- `/links` — полезные ссылки
- `/add_link` — добавить ссылку, только для admin/developer
- `/delete_link` — удалить ссылку, только для admin/developer
- `/users` — список пользователей, только для developer
- `/set_role` — изменить роль пользователя, только для developer
- `/me` — информация о пользователе
- `/stats` — статистика
- `/help` — список команд

## Стек

- Python
- aiogram
- SQLite
- python-dotenv

## Структура

- `main.py` — точка входа: инициализация БД, бота и диспетчера.
- `bot/` — конфиг и сборка общего роутера.
- `database/` — подключение к SQLite и создание таблиц.
- `users/` — `/start`, `/me`, `/users`, `/set_role`, `/stats` и роли.
- `schedule/` — `/today`, `/tomorrow` и чтение `schedule.json`.
- `deadlines/` — `/deadlines`, `/add_deadline`, `/delete_deadline`.
- `links/` — `/links`, `/add_link`, `/delete_link`.
- `common/` — общие команды, сейчас `/help`.

## Планы
- Расписание на неделю
- Рассылка объявлений
- Напоминания о дедлайнах
- Web-админка

## Запуск

1. Создать виртуальное окружение:

```bash
python -m venv .venv

.venv\Scripts\Activate.ps1
pip install -r requirements.txt
