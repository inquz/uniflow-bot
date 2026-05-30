from bot.config import ADMIN_IDS, DEVELOPER_IDS
from users.repository import get_user_by_telegram_id, set_user_role


def get_role(user_id: int) -> str | None:
    db_user = get_user_by_telegram_id(user_id)

    if db_user is None:
        return None

    return db_user["role"]


def is_admin(user_id: int) -> bool:
    return get_role(user_id) in {"admin", "developer"}


def is_developer(user_id: int) -> bool:
    return get_role(user_id) == "developer"


def sync_env_role(user_id: int) -> None:
    if user_id in DEVELOPER_IDS:
        set_user_role(user_id, "developer")
        return

    if user_id in ADMIN_IDS:
        db_user = get_user_by_telegram_id(user_id)

        if db_user is not None and db_user["role"] == "student":
            set_user_role(user_id, "admin")
