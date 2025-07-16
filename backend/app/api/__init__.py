"""
Importaciones de todas las rutas de la API.
"""

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.persons import router as persons_router
from app.api.audit import router as audit_router

__all__ = ["auth_router", "users_router", "persons_router", "audit_router"]
