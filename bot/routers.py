from aiogram import Router

from common.router import router as common_router
from deadlines.router import router as deadlines_router
from links.router import router as links_router
from schedule.router import router as schedule_router
from users.router import router as users_router


def build_router() -> Router:
    router = Router()

    router.include_router(users_router)
    router.include_router(schedule_router)
    router.include_router(deadlines_router)
    router.include_router(links_router)
    router.include_router(common_router)

    return router
