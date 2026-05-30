from typing import Any

from database.connection import get_connection


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
