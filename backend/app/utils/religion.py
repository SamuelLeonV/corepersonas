"""
Utilidades para hashing seguro de religión.
"""

import hashlib
import secrets
from typing import Tuple
from app.core.config import settings


class ReligionHasher:
    """Hasher para religión con salt"""
    
    @staticmethod
    def hash_religion(religion: str) -> Tuple[str, str]:
        """
        Generar hash irreversible de la religión con salt
        
        Returns:
            Tuple[str, str]: (hash, salt)
        """
        if not religion:
            return "", ""
        
        # Normalizar religión
        normalized_religion = religion.lower().strip()
        
        # Generar salt aleatorio
        salt = secrets.token_hex(settings.HASH_SALT_LENGTH // 2)
        
        # Combinar religión con salt
        religion_with_salt = f"{normalized_religion}{salt}"
        
        # Generar hash
        if settings.RELIGION_HASH_ALGORITHM == "ARGON2":
            hash_value = ReligionHasher._hash_argon2(religion_with_salt)
        else:
            hash_value = ReligionHasher._hash_sha256(religion_with_salt)
        
        return hash_value, salt
    
    @staticmethod
    def verify_religion(religion: str, stored_hash: str, salt: str) -> bool:
        """
        Verificar si una religión coincide con el hash almacenado
        
        Args:
            religion: Religión a verificar
            stored_hash: Hash almacenado
            salt: Salt usado para el hash
            
        Returns:
            bool: True si coincide, False si no
        """
        if not religion or not stored_hash or not salt:
            return False
        
        # Normalizar religión
        normalized_religion = religion.lower().strip()
        
        # Combinar religión con salt
        religion_with_salt = f"{normalized_religion}{salt}"
        
        # Generar hash
        if settings.RELIGION_HASH_ALGORITHM == "ARGON2":
            calculated_hash = ReligionHasher._hash_argon2(religion_with_salt)
        else:
            calculated_hash = ReligionHasher._hash_sha256(religion_with_salt)
        
        return calculated_hash == stored_hash
    
    @staticmethod
    def _hash_sha256(data: str) -> str:
        """Generar hash SHA256"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def _hash_argon2(data: str) -> str:
        """Generar hash Argon2"""
        try:
            import argon2
            
            ph = argon2.PasswordHasher(
                time_cost=settings.ARGON2_TIME_COST,
                memory_cost=settings.ARGON2_MEMORY_COST,
                parallelism=settings.ARGON2_PARALLELISM,
                hash_len=32,
                salt_len=16
            )
            
            return ph.hash(data)
        except ImportError:
            # Fallback a SHA256 si Argon2 no está disponible
            return ReligionHasher._hash_sha256(data)
    
    @staticmethod
    def get_religion_indicator(religion_hash: str) -> str:
        """
        Obtener indicador de religión desde hash
        
        Args:
            religion_hash: Hash de la religión
            
        Returns:
            str: Indicador de religión
        """
        if not religion_hash:
            return "no_especificada"
        
        # Usar primeros 8 caracteres del hash como indicador
        return f"hash_{religion_hash[:8]}"
    
    @staticmethod
    def get_valid_religions() -> list:
        """Obtener lista de religiones válidas"""
        return [
            'catolica', 'protestante', 'evangelica', 'ortodoxa', 'judia', 
            'islamica', 'budista', 'hinduista', 'testigo_de_jehova', 
            'mormon', 'pentecostal', 'adventista', 'anglicana', 'luterana', 
            'presbiteriana', 'metodista', 'bautista', 'ninguna', 'otra'
        ]
    
    @staticmethod
    def is_valid_religion(religion: str) -> bool:
        """Verificar si una religión es válida"""
        if not religion:
            return False
        
        normalized = religion.lower().strip()
        return normalized in ReligionHasher.get_valid_religions()

# Funciones de compatibilidad para testing
def validate_religion(religion: str) -> bool:
    """Función de compatibilidad para testing"""
    valid_religions = [
        "Católica", "Protestante", "Judía", "Musulmana", 
        "Budista", "Hinduista", "Otra", "Ninguna"
    ]
    return religion in valid_religions

def get_religion_hash(religion: str) -> str:
    """Función de compatibilidad para testing"""
    hasher = ReligionHasher()
    hash_value, _ = hasher.hash_religion(religion)
    return hash_value
