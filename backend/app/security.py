"""
Archivo de compatibilidad para mantener referencias existentes a app.security.
Exporta las clases de seguridad desde sus módulos correspondientes.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

# Importar las clases desde los módulos core
from app.core.security_service import SecurityService
from app.core.security_utils import SecurityUtils
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.config import settings

# Configurar logging
logger = logging.getLogger(__name__)

# Re-exportar para compatibilidad
__all__ = ["SecurityService", "SecurityUtils", "AuthService", "AuditService"]


class AuthService:
    """Servicio de autenticación"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Autenticar usuario"""
        user = self.db.query(User).filter(
            User.email == email,
            User.is_active == True
        ).first()
        
        if not user:
            return None
        
        # Verificar si el usuario está bloqueado
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Cuenta bloqueada temporalmente por múltiples intentos fallidos"
            )
        
        # Verificar contraseña
        if not SecurityUtils.verify_password(password, user.hashed_password):
            # Incrementar intentos fallidos
            user.login_attempts = (user.login_attempts or 0) + 1
            
            if user.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                # Bloquear cuenta
                user.locked_until = datetime.utcnow() + timedelta(seconds=settings.LOCKOUT_DURATION)
                logger.warning(f"Usuario bloqueado por múltiples intentos: {user.email}")
            
            self.db.commit()
            return None
        
        # Login exitoso - resetear intentos
        user.login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        return user
    
    def create_user(self, user_data: dict) -> User:
        """Crear nuevo usuario"""
        # Verificar que el email no exista
        existing_user = self.db.query(User).filter(User.email == user_data["email"]).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear usuario
        hashed_password = SecurityUtils.get_password_hash(user_data["password"])
        user = User(
            email=user_data["email"],
            hashed_password=hashed_password,
            is_active=user_data.get("is_active", True),
            is_admin=user_data.get("is_admin", False)
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user


class AuditService:
    """Servicio para logging de auditoría"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_action(
        self,
        user_id: Optional[int],
        action: str,
        resource: str,
        resource_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[str] = None
    ) -> None:
        """Registrar acción en log de auditoría"""
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        
        self.db.add(log_entry)
        self.db.commit()
    
    def get_audit_logs(
        self,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list:
        """Obtener logs de auditoría"""
        query = self.db.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if resource:
            query = query.filter(AuditLog.resource == resource)
        
        return query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
