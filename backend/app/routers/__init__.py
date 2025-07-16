"""
Routers package - Configuración de rutas de la API
"""

from .auth import router as auth_router
from .users import router as users_router  
from .persons import router as persons_router
from .audit import router as audit_router

__all__ = [
    "auth_router",
    "users_router", 
    "persons_router",
    "audit_router"
]
