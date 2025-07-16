"""
Constantes del sistema de auditoría de software
Mantiene sincronizadas las opciones entre frontend y backend
"""

from typing import List, Dict, Any

# Religiones válidas - sincronizado con frontend
RELIGION_OPTIONS = [
    {'value': 'catolica', 'label': 'Católica', 'category': 'cristianismo'},
    {'value': 'evangelica', 'label': 'Evangélica', 'category': 'cristianismo'},
    {'value': 'protestante', 'label': 'Protestante', 'category': 'cristianismo'},
    {'value': 'ortodoxa', 'label': 'Ortodoxa', 'category': 'cristianismo'},
    {'value': 'musulmana', 'label': 'Musulmana', 'category': 'islam'},
    {'value': 'judia', 'label': 'Judía', 'category': 'judaismo'},
    {'value': 'budista', 'label': 'Budista', 'category': 'budismo'},
    {'value': 'hindu', 'label': 'Hindú', 'category': 'hinduismo'},
    {'value': 'testigo_jehova', 'label': 'Testigo de Jehová', 'category': 'cristianismo'},
    {'value': 'mormon', 'label': 'Mormón', 'category': 'cristianismo'},
    {'value': 'adventista', 'label': 'Adventista', 'category': 'cristianismo'},
    {'value': 'bahai', 'label': 'Bahá\'í', 'category': 'otra'},
    {'value': 'sij', 'label': 'Sij', 'category': 'otra'},
    {'value': 'otra', 'label': 'Otra', 'category': 'otra'},
    {'value': 'agnostica', 'label': 'Agnóstica', 'category': 'ninguna'},
    {'value': 'atea', 'label': 'Atea', 'category': 'ninguna'},
    {'value': 'ninguna', 'label': 'Ninguna', 'category': 'ninguna'},
]

# Lista simple de valores válidos para validación
VALID_RELIGIONS = [option['value'] for option in RELIGION_OPTIONS]

# Categorías de religiones
RELIGION_CATEGORIES = {
    'cristianismo': 'Cristianismo',
    'islam': 'Islam',
    'judaismo': 'Judaísmo',
    'budismo': 'Budismo',
    'hinduismo': 'Hinduismo',
    'otra': 'Otra',
    'ninguna': 'Ninguna/No especificada'
}

def get_religion_label(value: str) -> str:
    """Obtener etiqueta legible de una religión por su valor"""
    for option in RELIGION_OPTIONS:
        if option['value'] == value:
            return option['label']
    return value.title()

def get_religion_category(value: str) -> str:
    """Obtener categoría de una religión por su valor"""
    for option in RELIGION_OPTIONS:
        if option['value'] == value:
            return RELIGION_CATEGORIES.get(option['category'], 'Otra')
    return 'Otra'

def validate_religion(value: str) -> bool:
    """Validar si una religión es válida"""
    return value.lower().strip() in VALID_RELIGIONS

# Configuración de RUT
RUT_VALIDATION = {
    'min_length': 8,
    'max_length': 12,
    'pattern': r'^\d{7,8}[0-9K]$',
    'mask_length': 4  # Caracteres a mostrar al final en RUT ofuscado
}

# Configuración de contraseñas
PASSWORD_VALIDATION = {
    'min_length': 8,
    'max_length': 100,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_number': True,
    'require_special_char': True,
    'special_chars': r'[!@#$%^&*(),.?":{}|<>]'
}

# Configuración de auditoría
AUDIT_ACTIONS = [
    'CREATE',
    'READ',
    'UPDATE',
    'DELETE',
    'LOGIN',
    'LOGOUT',
    'SEARCH'
]

# Configuración de seguridad
SECURITY_CONFIG = {
    'hash_algorithm': 'SHA256',
    'salt_length': 32,
    'bcrypt_rounds': 12,
    'max_login_attempts': 5,
    'lockout_duration': 900,  # 15 minutos en segundos
    'token_expire_minutes': 30
}
