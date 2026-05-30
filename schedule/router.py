from aiogram import Router

from schedule.today import router as today_router
from schedule.tomorrow import router as tomorrow_router

router = Router()

router.include_router(today_router)
router.include_router(tomorrow_router)
