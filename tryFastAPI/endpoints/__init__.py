from .ping import api_router as ping_router
from .http import api_router as html_router

all_routers = [ping_router, html_router]

__all__ = [all_routers]
