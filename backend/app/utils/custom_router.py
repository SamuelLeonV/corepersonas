"""
Router personalizado para manejar rutas con y sin barra final
"""

from fastapi import APIRouter as FastAPIRouter
from fastapi.routing import APIRoute
from typing import Callable, Any, Dict, List, Optional, Union
from starlette.routing import Match, Route
from starlette.requests import Request
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)

class CustomAPIRouter(FastAPIRouter):
    """
    Router personalizado que maneja automáticamente rutas con y sin barra final
    """
    
    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        methods: Optional[Union[set, List[str]]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Agregar ruta API con soporte automático para rutas con y sin barra final
        """
        # Agregar ruta original
        super().add_api_route(path, endpoint, methods=methods, **kwargs)
        
        # Si la ruta termina con /, agregar versión sin barra final
        if path.endswith("/") and path != "/":
            path_without_slash = path.rstrip("/")
            super().add_api_route(path_without_slash, endpoint, methods=methods, **kwargs)
            logger.debug(f"Ruta agregada: {path_without_slash} -> {endpoint}")
            
        # Si la ruta NO termina con /, agregar versión con barra final
        elif not path.endswith("/") and path != "":
            path_with_slash = path + "/"
            super().add_api_route(path_with_slash, endpoint, methods=methods, **kwargs)
            logger.debug(f"Ruta agregada: {path_with_slash} -> {endpoint}")
        
        logger.debug(f"Ruta agregada: {path} -> {endpoint}")


def create_persons_router():
    """
    Crear router de personas con manejo personalizado de rutas
    """
    # Importar aquí para evitar importaciones circulares
    from app.routers.persons import (
        create_person, list_persons, get_person, update_person, delete_person, search_by_rut
    )
    
    router = CustomAPIRouter()
    
    # Agregar rutas usando el método personalizado
    router.add_api_route("/", create_person, methods=["POST"])
    router.add_api_route("/", list_persons, methods=["GET"])
    router.add_api_route("/{person_id}", get_person, methods=["GET"])
    router.add_api_route("/{person_id}", update_person, methods=["PUT"])
    router.add_api_route("/{person_id}", delete_person, methods=["DELETE"])
    router.add_api_route("/search/rut", search_by_rut, methods=["GET"])
    
    return router


def create_auth_router():
    """
    Crear router de autenticación con manejo personalizado de rutas
    """
    from app.routers.auth import login, register, verify_token, refresh_token, logout, get_current_user_info
    
    router = CustomAPIRouter()
    
    router.add_api_route("/login", login, methods=["POST"])
    router.add_api_route("/register", register, methods=["POST"])
    router.add_api_route("/verify-token", verify_token, methods=["POST"])
    router.add_api_route("/refresh", refresh_token, methods=["POST"])
    router.add_api_route("/logout", logout, methods=["POST"])
    router.add_api_route("/me", get_current_user_info, methods=["GET"])
    
    return router


def create_users_router():
    """
    Crear router de usuarios con manejo personalizado de rutas
    """
    from app.routers.users import list_users, create_user, get_user, update_user, delete_user
    
    router = CustomAPIRouter()
    
    router.add_api_route("/", list_users, methods=["GET"])
    router.add_api_route("/", create_user, methods=["POST"])
    router.add_api_route("/{user_id}", get_user, methods=["GET"])
    router.add_api_route("/{user_id}", update_user, methods=["PUT"])
    router.add_api_route("/{user_id}", delete_user, methods=["DELETE"])
    
    return router


def create_audit_router():
    """
    Crear router de auditoría con manejo personalizado de rutas
    """
    from app.routers.audit import get_audit_logs, get_audit_log, get_audit_stats
    
    router = CustomAPIRouter()
    
    router.add_api_route("/logs", get_audit_logs, methods=["GET"])
    router.add_api_route("/logs/{log_id}", get_audit_log, methods=["GET"])
    router.add_api_route("/stats", get_audit_stats, methods=["GET"])
    
    return router
