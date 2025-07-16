"""
Modelo de auditoría para el sistema.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.db.database import Base


class AuditLog(Base):
    """Modelo de log de auditoría"""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # Puede ser None para acciones anónimas
    action = Column(String(50), nullable=False)  # CREATE, READ, UPDATE, DELETE, LOGIN, etc.
    resource = Column(String(50), nullable=False)  # persons, users, etc.
    resource_id = Column(Integer, nullable=True)  # ID del recurso afectado
    ip_address = Column(String(45), nullable=True)  # IPv4 o IPv6
    user_agent = Column(String(500), nullable=True)
    details = Column(Text, nullable=True)  # Detalles adicionales en JSON
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Índices para consultas de auditoría
    __table_args__ = (
        Index('idx_audit_user_action', 'user_id', 'action'),
        Index('idx_audit_resource', 'resource', 'resource_id'),
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_ip_address', 'ip_address'),
    )
