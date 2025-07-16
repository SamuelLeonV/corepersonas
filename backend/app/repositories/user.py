"""
Repositorio para operaciones de usuarios.
"""

from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repositorio para operaciones de usuarios"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_active_users(self, skip: int = 0, limit: int = 100):
        """Obtener usuarios activos"""
        return self.db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def create_user(self, user_data: UserCreate, hashed_password: str) -> User:
        """Crear nuevo usuario con contraseña hasheada"""
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=user_data.is_active,
            is_admin=user_data.is_admin
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_password(self, user: User, hashed_password: str) -> User:
        """Actualizar contraseña de usuario"""
        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def increment_login_attempts(self, user: User) -> User:
        """Incrementar intentos de login fallidos"""
        user.login_attempts += 1
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def reset_login_attempts(self, user: User) -> User:
        """Resetear intentos de login fallidos"""
        user.login_attempts = 0
        user.locked_until = None
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def lock_user(self, user: User, locked_until) -> User:
        """Bloquear usuario temporalmente"""
        user.locked_until = locked_until
        self.db.commit()
        self.db.refresh(user)
        return user
