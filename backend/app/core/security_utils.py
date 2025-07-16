"""
Utilidades de seguridad para el sistema.
"""

from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings
import hashlib
import secrets
import re
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Configuración de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityUtils:
    """Utilidades de seguridad"""
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generar hash de contraseña"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Validar fuerza de contraseña"""
        if len(password) < settings.MIN_PASSWORD_LENGTH:
            return False
        
        # Al menos una mayúscula
        if not re.search(r'[A-Z]', password):
            return False
        
        # Al menos una minúscula
        if not re.search(r'[a-z]', password):
            return False
        
        # Al menos un número
        if not re.search(r'\d', password):
            return False
        
        # Al menos un carácter especial
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            return False
        
        return True
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token JWT"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError as e:
            logger.warning(f"Token verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def generate_salt(length: int = 32) -> str:
        """Generar salt aleatorio"""
        return secrets.token_hex(length // 2)
    
    @staticmethod
    def hash_data(data: str, salt: str = None) -> str:
        """Hash de datos con salt opcional"""
        if salt:
            data_with_salt = f"{data}{salt}"
        else:
            data_with_salt = data
        
        return hashlib.sha256(data_with_salt.encode()).hexdigest()
    
    @staticmethod
    def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
        """Ofuscar datos sensibles"""
        if not data:
            return ""
        
        if len(data) <= visible_chars:
            return "*" * len(data)
        
        masked_chars = len(data) - visible_chars
        return "*" * masked_chars + data[-visible_chars:]
