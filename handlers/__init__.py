from handlers.commands import router as commands_router
from handlers.shop import router as shop_router
from handlers.combat import router as combat_router
from handlers.admin import router as admin_router

__all__ = [
    'commands_router',
    'shop_router',
    'combat_router',
    'admin_router'
]
