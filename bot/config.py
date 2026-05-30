import os

from dotenv import load_dotenv

load_dotenv()


def parse_ids(raw_ids: str) -> set[int]:
    return {
        int(item.strip())
        for item in raw_ids.split(",")
        if item.strip().isdigit()
    }


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = parse_ids(os.getenv("ADMIN_IDS", ""))
DEVELOPER_IDS = parse_ids(os.getenv("DEVELOPER_IDS", ""))
