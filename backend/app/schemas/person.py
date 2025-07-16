"""
Esquemas Pydantic para personas.
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime
import re


# Lista de religiones válidas
VALID_RELIGIONS = [
    'catolica', 'protestante', 'evangelica', 'ortodoxa', 'judia', 'islamica', 'budista', 'hinduista',
    'testigo_de_jehova', 'mormon', 'pentecostal', 'adventista', 'anglicana', 'luterana', 'presbiteriana',
    'metodista', 'bautista', 'ninguna', 'otra'
]


class PersonBase(BaseModel):
    """Esquema base para personas"""
    rut: str = Field(..., min_length=8, max_length=12)
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    religion: str = Field(..., min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=500)
    fecha_nacimiento: Optional[datetime] = None
    
    @validator('rut')
    def validate_rut(cls, v):
        """Validar RUT chileno"""
        if not v:
            raise ValueError('El RUT es requerido')
        
        # Limpiar RUT
        clean_rut = v.replace('.', '').replace('-', '').upper()
        
        if len(clean_rut) < 8 or len(clean_rut) > 9:
            raise ValueError('El RUT debe tener entre 8 y 9 caracteres')
        
        # Validar formato
        if not re.match(r'^\d{7,8}[0-9K]$', clean_rut):
            raise ValueError('Formato de RUT inválido')
        
        # Validar dígito verificador
        rut_digits = clean_rut[:-1]
        dv = clean_rut[-1]
        
        suma = 0
        multiplicador = 2
        
        for digit in reversed(rut_digits):
            suma += int(digit) * multiplicador
            multiplicador = multiplicador + 1 if multiplicador < 7 else 2
        
        resto = suma % 11
        dv_calculado = 'K' if resto == 1 else '0' if resto == 0 else str(11 - resto)
        
        if dv != dv_calculado:
            raise ValueError('RUT inválido')
        
        return clean_rut
    
    @validator('nombre', 'apellido')
    def validate_name(cls, v):
        """Validar nombres y apellidos"""
        if not v or not v.strip():
            raise ValueError('El nombre y apellido son requeridos')
        
        # Solo letras, espacios y algunos caracteres especiales
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\'\.]+$', v):
            raise ValueError('Solo se permiten letras, espacios y algunos caracteres especiales')
        
        return v.strip().title()
    
    @validator('religion')
    def validate_religion(cls, v):
        """Validar religión"""
        if not v or not v.strip():
            raise ValueError('La religión es requerida')
        
        if v.lower().strip() not in VALID_RELIGIONS:
            raise ValueError(f'Religión inválida. Opciones válidas: {", ".join(VALID_RELIGIONS)}')
        
        return v.lower().strip()
    
    @validator('telefono')
    def validate_telefono(cls, v):
        """Validar teléfono"""
        if v and not re.match(r'^[+]?[0-9\s\-\(\)]{7,20}$', v):
            raise ValueError('Formato de teléfono inválido')
        return v


class PersonCreate(PersonBase):
    """Esquema para crear personas"""
    class Config:
        json_schema_extra = {
            "example": {
                "rut": "12.345.678-9",
                "nombre": "Juan Carlos",
                "apellido": "Pérez González",
                "religion": "catolica",
                "email": "juan.perez@ejemplo.com",
                "telefono": "+56912345678",
                "direccion": "Av. Libertador Bernardo O'Higgins 123, Santiago",
                "fecha_nacimiento": "1990-05-15T00:00:00Z"
            }
        }


class PersonUpdate(BaseModel):
    """Esquema para actualizar personas"""
    rut: Optional[str] = Field(None, min_length=8, max_length=12)
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    religion: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=500)
    fecha_nacimiento: Optional[datetime] = None
    
    # Reutilizar validadores de PersonBase
    _validate_rut = validator('rut', allow_reuse=True)(PersonBase.__dict__['validate_rut'])
    _validate_name = validator('nombre', 'apellido', allow_reuse=True)(PersonBase.__dict__['validate_name'])
    _validate_religion = validator('religion', allow_reuse=True)(PersonBase.__dict__['validate_religion'])
    _validate_telefono = validator('telefono', allow_reuse=True)(PersonBase.__dict__['validate_telefono'])


class PersonResponse(BaseModel):
    """Esquema de respuesta para personas"""
    id: int
    rut: str = Field(..., description="RUT desencriptado y formateado")
    rut_masked: Optional[str] = Field(None, description="RUT ofuscado para mostrar")
    nombre: str
    apellido: str
    religion_indicator: Optional[str] = Field(None, description="Indicador de religión")
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PersonDetailResponse(BaseModel):
    """Esquema de respuesta detallada para personas"""
    id: int
    rut: str = Field(..., description="RUT desencriptado y formateado")
    rut_masked: Optional[str] = Field(None, description="RUT ofuscado para mostrar")
    nombre: str
    apellido: str
    religion_indicator: Optional[str] = Field(None, description="Indicador de religión")
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
