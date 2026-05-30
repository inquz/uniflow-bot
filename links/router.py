from aiogram import Router

from links.add_links import router as add_links_router
from links.delete_links import router as delete_links_router
from links.show_links import router as show_links_router

router = Router()

router.include_router(show_links_router)
router.include_router(add_links_router)
router.include_router(delete_links_router)
