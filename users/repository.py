from typing import Any

from database.connection import get_connection


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


def set_user_role(telegram_id: int, role: str) -> bool:
    allowed_roles = {"student", "admin", "developer"}

    if role not in allowed_roles:
        return False

    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE users
            SET role = ?
            WHERE telegram_id = ?
            """,
            (role, telegram_id),
        )

    return cursor.rowcount > 0


def get_users(limit: int = 50) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, telegram_id, username, first_name, role, created_at
            FROM users
            ORDER BY id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]
