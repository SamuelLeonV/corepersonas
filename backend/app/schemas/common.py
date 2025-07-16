"""
Esquemas Pydantic comunes para la aplicación.
"""

from pydantic import BaseModel
from typing import Optional, List, Any


class ApiResponse(BaseModel):
    """Esquema de respuesta genérica para la API"""
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None


class PaginatedResponse(BaseModel):
    """Esquema para respuestas paginadas"""
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class HealthCheckResponse(BaseModel):
    """Esquema para health check"""
    status: str
    timestamp: str
    version: str
    database: str
