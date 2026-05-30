from aiogram import Router

from common.help import router as help_router

router = Router()

router.include_router(help_router)
