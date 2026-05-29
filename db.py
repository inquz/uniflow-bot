import sqlite3
from pathlib import Path
from typing import Any
from datetime import datetime

DB_PATH = Path("data/uniflow.db")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                first_name TEXT,
                role TEXT NOT NULL DEFAULT 'student',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS deadlines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                title TEXT NOT NULL,
                due_at TEXT NOT NULL,
                created_by INTEGER NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT,
                created_by INTEGER NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
)


def add_user(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO users (telegram_id, username, first_name)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name
            """,
            (telegram_id, username, first_name),
        )


def get_user_by_telegram_id(telegram_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, telegram_id, username, first_name, role, created_at
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,),
        ).fetchone()

    if row is None:
        return None

    return dict(row)


def get_users_count() -> int:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            """
        ).fetchone()

    return int(row["count"])


def add_deadline(
    subject: str,
    title: str,
    due_at: str,
    created_by: int,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO deadlines (subject, title, due_at, created_by)
            VALUES (?, ?, ?, ?)
            """,
            (subject, title, due_at, created_by),
        )


def get_active_deadlines(limit: int = 10) -> list[dict[str, Any]]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, subject, title, due_at, created_by, created_at
            FROM deadlines
            WHERE is_active = 1
              AND due_at >= ?
            ORDER BY due_at ASC
            LIMIT ?
            """,
            (now, limit),
        ).fetchall()

    return [dict(row) for row in rows]

def deactivate_deadline(deadline_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE deadlines
            SET is_active = 0
            WHERE id = ?
              AND is_active = 1
            """,
            (deadline_id,),
        )

    return cursor.rowcount > 0    

def add_link(
    subject: str,
    title: str,
    url: str,
    description: str | None,
    created_by: int,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO links (subject, title, url, description, created_by)
            VALUES (?, ?, ?, ?, ?)
            """,
            (subject, title, url, description, created_by),
        )


def get_active_links(limit: int = 30) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, subject, title, url, description, created_by, created_at
            FROM links
            WHERE is_active = 1
            ORDER BY subject ASC, title ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def deactivate_link(link_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE links
            SET is_active = 0
            WHERE id = ?
              AND is_active = 1
            """,
            (link_id,),
        )

    return cursor.rowcount > 0    