"""
Modelo de persona para el sistema de auditoría.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.db.database import Base
import hashlib
import secrets


class Person(Base):
    """Modelo de persona"""
    
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos personales
    rut = Column(String(200), unique=True, index=True, nullable=False)  # Aumentado para RUT encriptado
    rut_hash = Column(String(64), nullable=False)  # Hash del RUT para búsquedas
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    
    # Datos sensibles
    religion_hash = Column(String(64), nullable=False)  # Hash irreversible de la religión
    religion_salt = Column(String(32), nullable=False)  # Salt para el hash
    
    # Datos adicionales (opcionales)
    email = Column(String(254), nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    fecha_nacimiento = Column(DateTime, nullable=True)
    
    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False)  # ID del usuario que creó el registro
    
    # Índices para optimización y seguridad
    __table_args__ = (
        Index('idx_person_rut_hash', 'rut_hash'),
        Index('idx_person_nombre_apellido', 'nombre', 'apellido'),
        Index('idx_person_created_at', 'created_at'),
        Index('idx_person_created_by', 'created_by'),
    )
    
    def set_religion_hash(self, religion: str) -> None:
        """Genera hash irreversible de la religión usando el servicio de seguridad"""
        if religion:
            # Usar el servicio de seguridad centralizado
            from app.core.security_service import SecurityService
            religion_hash, salt = SecurityService.hash_religion(religion)
            self.religion_hash = religion_hash
            self.religion_salt = salt
        else:
            self.religion_salt = ""
            self.religion_hash = ""
    
    def set_rut_hash(self, rut: str) -> None:
        """Genera hash del RUT para búsquedas usando el servicio de seguridad"""
        if rut:
            # Usar el servicio de seguridad centralizado
            from app.core.security_service import SecurityService
            self.rut_hash = SecurityService.hash_rut(rut)
        else:
            self.rut_hash = ""
