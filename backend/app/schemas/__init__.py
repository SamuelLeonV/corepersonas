"""
Importaciones de todos los esquemas para facilitar el acceso.
"""

from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse, LoginRequest, Token, TokenData
from app.schemas.person import PersonBase, PersonCreate, PersonUpdate, PersonResponse, PersonDetailResponse
from app.schemas.audit import AuditLogResponse, AuditLogStatsResponse
from app.schemas.common import ApiResponse, PaginatedResponse, HealthCheckResponse

__all__ = [
    # User schemas
    "UserBase", "UserCreate", "UserUpdate", "UserResponse", "LoginRequest", "Token", "TokenData",
    # Person schemas
    "PersonBase", "PersonCreate", "PersonUpdate", "PersonResponse", "PersonDetailResponse",
    # Audit schemas
    "AuditLogResponse", "AuditLogStatsResponse",
    # Common schemas
    "ApiResponse", "PaginatedResponse", "HealthCheckResponse"
]
