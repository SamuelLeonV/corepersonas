"""
Servicio de autenticación y autorización.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime, timedelta
from app.models.user import User
from app.schemas.user import UserCreate, Token
from app.repositories.user import UserRepository
from app.repositories.audit import AuditRepository
from app.core.security_utils import SecurityUtils
from app.core.config import settings


class AuthService:
    """Servicio de autenticación y autorización"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditRepository(db)
    
    def login(self, email: str, password: str, ip_address: str = None, user_agent: str = None) -> Token:
        """Iniciar sesión"""
        from app.services.user import UserService
        
        user_service = UserService(self.db)
        user = user_service.authenticate_user(email, password, ip_address, user_agent)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        # Crear log de auditoría para login exitoso
        self.audit_repo.create_log(
            user_id=user.id,
            action="LOGIN",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=f"Login exitoso: {user.email}"
        )
        
        # Crear token de acceso
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = SecurityUtils.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    def register(self, user_data: UserCreate, ip_address: str = None) -> Token:
        """Registrar nuevo usuario"""
        # Verificar si el email ya existe
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Validar fuerza de contraseña
        if not SecurityUtils.validate_password_strength(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña no cumple con los requisitos de seguridad"
            )
        
        # Crear hash de contraseña
        hashed_password = SecurityUtils.get_password_hash(user_data.password)
        
        # Crear usuario (por defecto no es admin)
        user_data.is_admin = False
        user = self.user_repo.create_user(user_data, hashed_password)
        
        # Crear log de auditoría
        self.audit_repo.create_log(
            user_id=user.id,
            action="REGISTER",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            details=f"Usuario registrado: {user.email}"
        )
        
        # Crear token de acceso
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = SecurityUtils.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    def verify_token(self, token: str, ip_address: str = None, user_agent: str = None) -> dict:
        """Verificar token JWT"""
        try:
            payload = SecurityUtils.verify_token(token)
            
            # Crear log de auditoría para verificación exitosa
            user_email = payload.get("sub")
            if user_email:
                user = self.user_repo.get_by_email(user_email)
                if user:
                    self.audit_repo.create_log(
                        user_id=user.id,
                        action="VERIFY_TOKEN",
                        resource="users",
                        resource_id=user.id,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        details=f"Token verificado exitosamente: {user_email}"
                    )
            
            return {"valid": True, "payload": payload}
        except HTTPException:
            # Log de verificación fallida (sin user_id porque no se pudo verificar)
            self.audit_repo.create_log(
                user_id=None,
                action="VERIFY_TOKEN",
                resource="users",
                ip_address=ip_address,
                user_agent=user_agent,
                details="Token inválido o expirado"
            )
            return {"valid": False, "payload": None}
    
    def logout(self, user_id: int, ip_address: str = None) -> bool:
        """Cerrar sesión"""
        # Crear log de auditoría
        self.audit_repo.create_log(
            user_id=user_id,
            action="LOGOUT",
            resource="users",
            resource_id=user_id,
            ip_address=ip_address,
            details="Sesión cerrada"
        )
        
        # En una implementación real, aquí se invalidaría el token
        # Por ahora solo registramos el logout
        return True
    
    def get_current_user(self, token: str) -> User:
        """Obtener usuario actual desde token"""
        payload = SecurityUtils.verify_token(token)
        email = payload.get("sub")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = self.user_repo.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        return user
    
    def refresh_token(self, token: str) -> Token:
        """Renovar token"""
        user = self.get_current_user(token)
        
        # Crear nuevo token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = SecurityUtils.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        # Crear log de auditoría
        self.audit_repo.create_log(
            user_id=user.id,
            action="REFRESH_TOKEN",
            resource="users",
            resource_id=user.id,
            details="Token renovado"
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    def authenticate_user(self, email: str, password: str, ip_address: str = None, user_agent: str = None) -> Optional[User]:
        """Autenticar usuario"""
        # Obtener usuario directamente del repositorio (modelo SQLAlchemy)
        user = self.user_repo.get_by_email(email)
        
        if not user:
            return None
            
        # Verificar contraseña
        if not SecurityUtils.verify_password(password, user.hashed_password):
            return None
            
        if not user.is_active:
            return None
            
        # Actualizar último login
        user.last_login = datetime.utcnow()
        user.login_attempts = 0  # Reset attempts on successful login
        self.db.commit()
        
        return user
