from datetime import datetime
from typing import Any

from database.connection import get_connection


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
