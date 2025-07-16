"""
Configuración global de la aplicación usando Pydantic BaseSettings.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME: str = "Sistema de Auditoría de Software - API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API REST segura para el sistema de auditoría de software - Parte 2"
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Configuración de la base de datos
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/auditoria_db"
    DATABASE_ECHO: bool = False
    
    # Configuración de autenticación JWT
    SECRET_KEY: str = "your-super-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001,http://localhost:5173"
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE"]
    CORS_HEADERS: List[str] = ["*"]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte la cadena de orígenes CORS separada por comas a una lista"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Configuración de Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Configuración de seguridad
    BCRYPT_ROUNDS: int = 12
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION: int = 900
    
    # Configuración de validaciones
    MIN_PASSWORD_LENGTH: int = 8
    MAX_NAME_LENGTH: int = 100
    MAX_EMAIL_LENGTH: int = 254
    
    # Configuración específica para datos sensibles
    RUT_MASK_LENGTH: int = 4
    RELIGION_HASH_ALGORITHM: str = "ARGON2"  # SHA256 o ARGON2
    HASH_SALT_LENGTH: int = 32
    
    # Configuración de encriptación de RUT (reversible con salt + pepper)
    RUT_ENCRYPTION_KEY: str = "your-super-secret-key-here-change-in-production"
    RUT_ENCRYPTION_SALT: str = "sistema_auditoria_salt"
    RUT_ENCRYPTION_ITERATIONS: int = 100000
    
    # Configuración específica para Argon2 (cuando RELIGION_HASH_ALGORITHM=ARGON2)
    ARGON2_TIME_COST: int = 2  # Número de iteraciones
    ARGON2_MEMORY_COST: int = 65536  # Memoria en KB (64MB)
    ARGON2_PARALLELISM: int = 1  # Número de threads paralelos
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
