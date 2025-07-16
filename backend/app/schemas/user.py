"""
Esquemas Pydantic para usuarios.
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime
import re


class UserBase(BaseModel):
    """Esquema base para usuarios"""
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    """Esquema para crear usuarios"""
    password: str = Field(..., min_length=8, max_length=100, description="Contraseña segura con al menos 8 caracteres")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "MiPassword123!",
                "is_active": True,
                "is_admin": False
            }
        }
    
    @validator('password')
    def validate_password(cls, v):
        """Validar fuerza de contraseña"""
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe contener al menos una minúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', v):
            raise ValueError('La contraseña debe contener al menos un carácter especial')
        return v


class UserUpdate(BaseModel):
    """Esquema para actualizar usuarios"""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        """Validar fuerza de contraseña"""
        if v is not None:
            if len(v) < 8:
                raise ValueError('La contraseña debe tener al menos 8 caracteres')
            if not re.search(r'[A-Z]', v):
                raise ValueError('La contraseña debe contener al menos una mayúscula')
            if not re.search(r'[a-z]', v):
                raise ValueError('La contraseña debe contener al menos una minúscula')
            if not re.search(r'\d', v):
                raise ValueError('La contraseña debe contener al menos un número')
            if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', v):
                raise ValueError('La contraseña debe contener al menos un carácter especial')
        return v


class UserResponse(UserBase):
    """Esquema de respuesta para usuarios"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Esquema para solicitud de login"""
    email: EmailStr = Field(..., description="Email del usuario registrado")
    password: str = Field(..., description="Contraseña del usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@auditoria.com",
                "password": "admin123"
            }
        }


class Token(BaseModel):
    """Esquema para token de acceso"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Esquema para datos del token"""
    email: Optional[str] = None
