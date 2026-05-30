from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from links.repository import get_active_links

router = Router()


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
