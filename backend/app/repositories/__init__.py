"""
Importaciones de todos los repositorios.
"""

from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository
from app.repositories.person import PersonRepository
from app.repositories.audit import AuditRepository

__all__ = ["BaseRepository", "UserRepository", "PersonRepository", "AuditRepository"]
