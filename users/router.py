from aiogram import Router

from users.list_users import router as list_users_router
from users.me import router as me_router
from users.set_role import router as set_role_router
from users.start import router as start_router
from users.stats import router as stats_router

router = Router()

router.include_router(start_router)
router.include_router(list_users_router)
router.include_router(set_role_router)
router.include_router(me_router)
router.include_router(stats_router)
