"""
Utilidades para respuestas de la API.
"""

from typing import Any, Optional, List
from app.schemas.common import ApiResponse, PaginatedResponse


class ResponseUtils:
    """Utilidades para respuestas de la API"""
    
    @staticmethod
    def success_response(message: str, data: Any = None) -> ApiResponse:
        """Crear respuesta exitosa"""
        return ApiResponse(
            success=True,
            message=message,
            data=data
        )
    
    @staticmethod
    def error_response(message: str, errors: Optional[List[str]] = None) -> ApiResponse:
        """Crear respuesta de error"""
        return ApiResponse(
            success=False,
            message=message,
            errors=errors or []
        )
    
    @staticmethod
    def paginated_response(
        items: List[Any],
        total: int,
        page: int,
        per_page: int
    ) -> PaginatedResponse:
        """Crear respuesta paginada"""
        pages = (total + per_page - 1) // per_page  # Ceiling division
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )
    
    @staticmethod
    def calculate_pagination(page: int, per_page: int) -> tuple:
        """Calcular skip y limit para paginación"""
        page = max(1, page)  # Asegurar que page sea al menos 1
        per_page = min(max(1, per_page), 100)  # Limitar per_page entre 1 y 100
        
        skip = (page - 1) * per_page
        limit = per_page
        
        return skip, limit

# Funciones de compatibilidad para testing
def create_success_response(data: Any, message: Optional[str] = None) -> dict:
    """Función de compatibilidad para testing"""
    response = {
        "success": True,
        "data": data
    }
    if message:
        response["message"] = message
    return response

def create_error_response(error: str, code: Optional[int] = None) -> dict:
    """Función de compatibilidad para testing"""
    response = {
        "success": False,
        "error": error
    }
    if code:
        response["code"] = code
    return response
