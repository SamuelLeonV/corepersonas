"""
Servicio de seguridad para operaciones criptográficas y de protección de datos.
"""

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
import logging
import re
import hashlib
import secrets

# Configurar logging
logger = logging.getLogger(__name__)

class SecurityService:
    """
    Servicio para operaciones de seguridad como encriptación y desencriptación
    """
    
    # Clave derivada para operaciones de cifrado
    __key = None
    
    @classmethod
    def __get_key(cls):
        """
        Obtener o generar clave de encriptación para RUT
        """
        if cls.__key is None:
            # Derivamos una clave a partir del RUT_ENCRYPTION_KEY
            salt = settings.RUT_ENCRYPTION_SALT.encode()
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=settings.RUT_ENCRYPTION_ITERATIONS,
            )
            key = base64.urlsafe_b64encode(kdf.derive(settings.RUT_ENCRYPTION_KEY.encode()))
            cls.__key = key
        return cls.__key
    
    @classmethod
    def encrypt_rut(cls, rut: str) -> str:
        """
        Encripta un RUT utilizando Fernet (AES-256)
        """
        if not rut:
            return ""
            
        try:
            key = cls.__get_key()
            f = Fernet(key)
            encrypted_data = f.encrypt(rut.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Error al encriptar RUT: {str(e)}")
            return ""
    
    @classmethod
    def decrypt_rut(cls, encrypted_rut: str) -> str:
        """
        Desencripta un RUT utilizando Fernet (AES-256)
        """
        if not encrypted_rut:
            return ""
            
        try:
            key = cls.__get_key()
            f = Fernet(key)
            # Convertir de base64 y desencriptar
            encrypted_data = base64.urlsafe_b64decode(encrypted_rut)
            decrypted_data = f.decrypt(encrypted_data)
            decrypted_rut = decrypted_data.decode()
            
            # Validar que el RUT desencriptado tiene sentido
            if len(decrypted_rut) > 50 or not any(c.isdigit() for c in decrypted_rut):
                logger.warning(f"RUT desencriptado parece inválido: {decrypted_rut[:20]}...")
                return "RUT_CORRUPTED"
                
            return decrypted_rut
        except Exception as e:
            logger.error(f"Error al desencriptar RUT: {str(e)}")
            return "RUT_DECRYPT_ERROR"  # Devolver un valor claro en lugar del encriptado
    
    @classmethod
    def clean_rut(cls, rut: str) -> str:
        """
        Limpia un RUT de puntos y guiones
        """
        if not rut:
            return ""
        return re.sub(r'[^0-9kK]', '', rut)
    
    @classmethod
    def format_rut(cls, rut: str) -> str:
        """
        Formatea un RUT en formato XX.XXX.XXX-Y
        """
        if not rut:
            return ""
            
        clean = cls.clean_rut(rut)
        if len(clean) <= 1:
            return clean
            
        dv = clean[-1]
        num = clean[:-1]
        
        # Formatear con puntos y guión
        formatted = ""
        for i in range(len(num), 0, -3):
            if i >= 3:
                formatted = "." + num[max(i-3, 0):i] + formatted
            else:
                formatted = num[0:i] + formatted
                
        if formatted.startswith("."):
            formatted = formatted[1:]
            
        return f"{formatted}-{dv}"
    
    @classmethod
    def validate_rut(cls, rut: str) -> bool:
        """
        Valida un RUT chileno
        """
        if not rut:
            return False
            
        clean = cls.clean_rut(rut)
        
        # Validar formato
        pattern = re.compile(r'^[0-9]{1,8}[0-9kK]$')
        if not pattern.match(clean):
            return False
            
        # Separar número de dígito verificador
        rut_number = clean[:-1]
        dv = clean[-1].upper()
        
        # Cálculo del dígito verificador
        serie = [2, 3, 4, 5, 6, 7]
        sum = 0
        
        for i in range(len(rut_number)):
            sum += int(rut_number[-(i+1)]) * serie[i % len(serie)]
            
        calculated_dv = 11 - (sum % 11)
        
        if calculated_dv == 11:
            calculated_dv = '0'
        elif calculated_dv == 10:
            calculated_dv = 'K'
        else:
            calculated_dv = str(calculated_dv)
            
        return calculated_dv == dv
    
    @classmethod
    def mask_rut(cls, rut: str) -> str:
        """
        Ofusca un RUT mostrando solo los últimos dígitos
        """
        if not rut:
            return ""
            
        clean = cls.clean_rut(rut)
        if len(clean) <= settings.RUT_MASK_LENGTH:
            return "*" * len(clean)
            
        visible_chars = settings.RUT_MASK_LENGTH
        masked_chars = len(clean) - visible_chars
        
        return "*" * masked_chars + clean[-visible_chars:]
    
    @classmethod
    def hash_religion(cls, religion: str, salt: str = None) -> tuple:
        """
        Genera hash irreversible de religión con salt usando el algoritmo configurado
        """
        if not religion:
            return "", ""
            
        # Generar salt si no se proporciona
        if salt is None:
            salt = secrets.token_hex(settings.HASH_SALT_LENGTH // 2)
            
        # Normalizar religión
        religion_normalized = religion.lower().strip()
        
        # Usar el algoritmo configurado
        if settings.RELIGION_HASH_ALGORITHM == "ARGON2":
            try:
                import argon2
                ph = argon2.PasswordHasher(
                    time_cost=settings.ARGON2_TIME_COST,
                    memory_cost=settings.ARGON2_MEMORY_COST,
                    parallelism=settings.ARGON2_PARALLELISM,
                    hash_len=32,
                    salt_len=16
                )
                # Combinar religión con salt personalizado
                religion_with_salt = f"{religion_normalized}{salt}"
                religion_hash = ph.hash(religion_with_salt)
                # Extraer solo el hash sin metadatos de argon2
                hash_parts = religion_hash.split('$')
                if len(hash_parts) >= 6:
                    religion_hash = hash_parts[-1]  # Solo el hash final
                else:
                    religion_hash = hashlib.sha256(religion_with_salt.encode()).hexdigest()
            except ImportError:
                logger.warning("Argon2 no disponible, usando SHA256 como fallback")
                religion_with_salt = f"{religion_normalized}{salt}"
                religion_hash = hashlib.sha256(religion_with_salt.encode()).hexdigest()
        else:
            # Usar SHA256 como fallback
            religion_with_salt = f"{religion_normalized}{salt}"
            religion_hash = hashlib.sha256(religion_with_salt.encode()).hexdigest()
            
        return religion_hash, salt
    
    @classmethod
    def generate_religion_indicator(cls, religion_hash: str) -> str:
        """
        Genera un indicador de religión a partir del hash
        """
        if not religion_hash:
            return "no_especificada"
            
        # Usar los primeros caracteres como identificador anónimo
        return f"hash_{religion_hash[:8]}"
    
    @classmethod
    def hash_rut(cls, rut: str) -> str:
        """
        Genera hash de RUT para búsquedas
        """
        if not rut:
            return ""
            
        clean_rut = cls.clean_rut(rut)
        return hashlib.sha256(clean_rut.encode()).hexdigest()
