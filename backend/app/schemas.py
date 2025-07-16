"""
Esquemas Pydantic para validación de datos.
"""

from pydantic import BaseModel, EmailStr, Field, validator, SecretStr
from typing import Optional, List, Any, Union
from datetime import datetime, date
import re


# Funciones de validación de RUT chileno

def clean_rut(rut: str) -> str:
    """Limpia un RUT de puntos y guiones, dejando solo dígitos y el dígito verificador"""
    return re.sub(r'[^0-9kK]', '', rut)

def validate_rut_format(rut: str) -> bool:
    """Validación de formato de RUT chileno"""
    rut_pattern = re.compile(r'^[0-9]{1,8}-?[0-9kK]$')
    return bool(rut_pattern.match(clean_rut(rut)))

def calculate_rut_dv(rut_number: int) -> str:
    """Calcula el dígito verificador de un RUT"""
    serie = [2, 3, 4, 5, 6, 7]
    sum = 0
    
    for i in range(len(str(rut_number))):
        sum += int(str(rut_number)[-1-i]) * serie[i % len(serie)]
    
    res = 11 - (sum % 11)
    
    if res == 11:
        return '0'
    elif res == 10:
        return 'K'
    else:
        return str(res)

def validate_rut(rut: str) -> bool:
    """Validación completa de RUT chileno: formato y dígito verificador"""
    if not rut:
        return False
    
    clean = clean_rut(rut)
    
    # Validar formato
    if not validate_rut_format(clean):
        return False
    
    # Separar número de dígito verificador
    if '-' in clean:
        rut_number, dv = clean.split('-')
    else:
        rut_number = clean[:-1]
        dv = clean[-1]
    
    # Validar dígito verificador
    calculated_dv = calculate_rut_dv(int(rut_number))
    return calculated_dv.upper() == dv.upper()


# Esquemas de Usuario

class UserBase(BaseModel):
    """Esquema base de usuario"""
    email: EmailStr


class UserCreate(UserBase):
    """Esquema de creación de usuario"""
    password: str = Field(..., min_length=8)
    is_admin: Optional[bool] = False
    
    @validator('password')
    def password_strength(cls, v):
        """Validar fuerza de contraseña"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', v):
            raise ValueError('La contraseña debe contener al menos un carácter especial')
        return v


class UserUpdate(BaseModel):
    """Esquema de actualización de usuario"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    
    @validator('password')
    def password_strength(cls, v):
        if v is not None:
            if len(v) < 8:
                raise ValueError('La contraseña debe tener al menos 8 caracteres')
            if not re.search(r'[A-Z]', v):
                raise ValueError('La contraseña debe contener al menos una letra mayúscula')
            if not re.search(r'[a-z]', v):
                raise ValueError('La contraseña debe contener al menos una letra minúscula')
            if not re.search(r'\d', v):
                raise ValueError('La contraseña debe contener al menos un número')
            if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', v):
                raise ValueError('La contraseña debe contener al menos un carácter especial')
        return v


class UserInDB(UserBase):
    """Esquema de usuario en base de datos"""
    id: int
    is_active: bool
    is_admin: bool
    login_attempts: int
    locked_until: Optional[datetime] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class UserResponse(UserBase):
    """Esquema de respuesta de usuario"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        orm_mode = True


# Esquemas de Persona

class PersonBase(BaseModel):
    """Esquema base de persona"""
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None


class PersonCreate(PersonBase):
    """Esquema de creación de persona"""
    rut: str = Field(..., min_length=8, max_length=12)
    religion: Optional[str] = None
    
    @validator('rut')
    def validate_rut_field(cls, v):
        """Validar RUT chileno"""
        if not validate_rut(v):
            raise ValueError('RUT inválido')
        return v


class PersonUpdate(BaseModel):
    """Esquema de actualización de persona"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    religion: Optional[str] = None


class PersonResponse(PersonBase):
    """Esquema de respuesta de persona (sin datos sensibles)"""
    id: int
    rut_masked: str
    religion_indicator: str
    created_at: datetime
    created_by: int
    
    class Config:
        orm_mode = True


class PersonDetailResponse(PersonResponse):
    """Esquema de respuesta detallada de persona (con datos sensibles ofuscados)"""
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


# Esquemas de Autenticación

class Token(BaseModel):
    """Esquema de token de acceso"""
    access_token: str
    token_type: str
    expires_at: datetime
    user: UserResponse


class TokenPayload(BaseModel):
    """Esquema de payload de token"""
    sub: Optional[str] = None
    exp: Optional[int] = None


# Esquemas de Auditoría

class AuditLogBase(BaseModel):
    """Esquema base de log de auditoría"""
    action: str
    resource: str
    resource_id: Optional[int] = None
    details: Optional[Any] = None


class AuditLogCreate(AuditLogBase):
    """Esquema de creación de log de auditoría"""
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    """Esquema de respuesta de log de auditoría"""
    id: int
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime
    
    class Config:
        orm_mode = True


# Esquemas de respuesta general

class APIResponse(BaseModel):
    """Esquema de respuesta general de la API"""
    success: bool
    message: str
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    """Esquema de respuesta paginada"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
