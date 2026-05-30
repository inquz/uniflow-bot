from aiogram import Router

from deadlines.add_deadlines import router as add_deadlines_router
from deadlines.delete_deadlines import router as delete_deadlines_router
from deadlines.show_deadlines import router as show_deadlines_router

router = Router()

router.include_router(show_deadlines_router)
router.include_router(add_deadlines_router)
router.include_router(delete_deadlines_router)
