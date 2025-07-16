"""
Servicio para operaciones de usuarios.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List
from datetime import datetime, timedelta
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.repositories.user import UserRepository
from app.repositories.audit import AuditRepository
from app.core.security_utils import SecurityUtils
from app.core.config import settings


class UserService:
    """Servicio para operaciones de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditRepository(db)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Obtener lista de usuarios"""
        users = self.user_repo.get_multi(skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Obtener usuario por ID"""
        user = self.user_repo.get(user_id)
        if user:
            return UserResponse.model_validate(user)
        return None
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Obtener usuario por email"""
        user = self.user_repo.get_by_email(email)
        if user:
            return UserResponse.model_validate(user)
        return None
    
    def create_user(self, user_data: UserCreate, created_by: int, ip_address: str = None) -> UserResponse:
        """Crear nuevo usuario"""
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
        
        # Crear usuario
        user = self.user_repo.create_user(user_data, hashed_password)
        
        # Crear log de auditoría
        self.audit_repo.create_log(
            user_id=created_by,
            action="CREATE",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            details=f"Usuario creado: {user.email}"
        )
        
        return UserResponse.model_validate(user)
    
    def create_user_direct(self, user_data: UserCreate) -> User:
        """Crear usuario directamente para pruebas (sin auditoría)"""
        # Verificar si el email ya existe
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear hash de contraseña
        hashed_password = SecurityUtils.get_password_hash(user_data.password)
        
        # Crear usuario directamente
        user = self.user_repo.create_user(user_data, hashed_password)
        
        return user
    
    def update_user(self, user_id: int, user_data: UserUpdate, updated_by: int, ip_address: str = None) -> UserResponse:
        """Actualizar usuario"""
        user = self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar si el nuevo email ya existe
        if user_data.email and user_data.email != user.email:
            if self.user_repo.get_by_email(user_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
        
        # Actualizar contraseña si se proporciona
        if user_data.password:
            if not SecurityUtils.validate_password_strength(user_data.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La contraseña no cumple con los requisitos de seguridad"
                )
            hashed_password = SecurityUtils.get_password_hash(user_data.password)
            user = self.user_repo.update_password(user, hashed_password)
        
        # Actualizar otros campos
        updated_user = self.user_repo.update(user, user_data)
        
        # Crear log de auditoría
        self.audit_repo.create_log(
            user_id=updated_by,
            action="UPDATE",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            details=f"Usuario actualizado: {user.email}"
        )
        
        return UserResponse.model_validate(updated_user)
    
    def delete_user(self, user_id: int, deleted_by: int, ip_address: str = None) -> bool:
        """Eliminar usuario"""
        user = self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # No permitir eliminar el último administrador
        if user.is_admin:
            admin_count = len([u for u in self.user_repo.get_multi(skip=0, limit=1000) if u.is_admin and u.id != user_id])
            if admin_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede eliminar el último administrador"
                )
        
        # Crear log de auditoría
        self.audit_repo.create_log(
            user_id=deleted_by,
            action="DELETE",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            details=f"Usuario eliminado: {user.email}"
        )
        
        # Eliminar usuario
        self.user_repo.delete(user_id)
        return True
    
    def authenticate_user(self, email: str, password: str, ip_address: str = None, user_agent: str = None) -> Optional[User]:
        """Autenticar usuario"""
        user = self.user_repo.get_by_email(email)
        
        if not user:
            # Log de intento de login fallido
            self.audit_repo.create_log(
                user_id=None,
                action="LOGIN_FAILED",
                resource="users",
                ip_address=ip_address,
                user_agent=user_agent,
                details=f"Intento de login fallido para email: {email}"
            )
            return None
        
        # Verificar si el usuario está bloqueado
        if user.locked_until and user.locked_until > datetime.utcnow():
            # Log de intento de login con usuario bloqueado
            self.audit_repo.create_log(
                user_id=user.id,
                action="LOGIN_BLOCKED",
                resource="users",
                ip_address=ip_address,
                user_agent=user_agent,
                details=f"Intento de login con usuario bloqueado: {email}"
            )
            return None
        
        # Verificar contraseña
        if not SecurityUtils.verify_password(password, user.hashed_password):
            # Incrementar intentos fallidos
            self.user_repo.increment_login_attempts(user)
            
            # Bloquear usuario si supera el límite
            if user.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                locked_until = datetime.utcnow() + timedelta(seconds=settings.LOCKOUT_DURATION)
                self.user_repo.lock_user(user, locked_until)
            
            # Log de intento de login fallido
            self.audit_repo.create_log(
                user_id=user.id,
                action="LOGIN_FAILED",
                resource="users",
                ip_address=ip_address,
                user_agent=user_agent,
                details=f"Contraseña incorrecta para: {email}"
            )
            return None
        
        # Login exitoso
        self.user_repo.reset_login_attempts(user)
        user.last_login = datetime.utcnow()
        self.user_repo.update(user, UserUpdate())
        
        # Log de login exitoso
        self.audit_repo.create_log(
            user_id=user.id,
            action="LOGIN_SUCCESS",
            resource="users",
            ip_address=ip_address,
            user_agent=user_agent,
            details=f"Login exitoso para: {email}"
        )
        
        return user
    
    def get_current_user_info(self, user_id: int, ip_address: str = None) -> UserResponse:
        """Obtener información del usuario actual"""
        user = self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Log de consulta de información personal
        self.audit_repo.create_log(
            user_id=user.id,
            action="READ",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            details="Consulta de información personal"
        )
        
        return UserResponse.model_validate(user)
