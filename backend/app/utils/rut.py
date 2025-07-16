"""
Utilidades para validación de RUT chileno.
"""

import re
from typing import Optional


class RutValidator:
    """Validador de RUT chileno"""
    
    @staticmethod
    def clean_rut(rut: str) -> str:
        """Limpiar RUT eliminando puntos y guiones"""
        if not rut:
            return ""
        return rut.replace(".", "").replace("-", "").upper().strip()
    
    @staticmethod
    def format_rut(rut: str) -> str:
        """Formatear RUT con puntos y guión"""
        clean = RutValidator.clean_rut(rut)
        if len(clean) < 8:
            return rut
        
        # Separar número y dígito verificador
        numero = clean[:-1]
        dv = clean[-1]
        
        # Agregar puntos cada 3 dígitos desde la derecha
        formatted = ""
        for i, digit in enumerate(reversed(numero)):
            if i > 0 and i % 3 == 0:
                formatted = "." + formatted
            formatted = digit + formatted
        
        return f"{formatted}-{dv}"
    
    @staticmethod
    def validate_rut(rut: str) -> bool:
        """Validar RUT chileno"""
        if not rut:
            return False
        
        clean_rut = RutValidator.clean_rut(rut)
        
        # Verificar longitud
        if len(clean_rut) < 8 or len(clean_rut) > 9:
            return False
        
        # Verificar formato
        if not re.match(r'^\d{7,8}[0-9K]$', clean_rut):
            return False
        
        # Validar dígito verificador
        return RutValidator.validate_dv(clean_rut)
    
    @staticmethod
    def validate_dv(rut: str) -> bool:
        """Validar dígito verificador del RUT"""
        if len(rut) < 8:
            return False
        
        rut_digits = rut[:-1]
        dv = rut[-1]
        
        try:
            suma = 0
            multiplicador = 2
            
            for digit in reversed(rut_digits):
                suma += int(digit) * multiplicador
                multiplicador = multiplicador + 1 if multiplicador < 7 else 2
            
            resto = suma % 11
            dv_calculado = 'K' if resto == 1 else '0' if resto == 0 else str(11 - resto)
            
            return dv == dv_calculado
        except (ValueError, IndexError):
            return False
    
    @staticmethod
    def generate_dv(rut_number: str) -> str:
        """Generar dígito verificador para un número de RUT"""
        try:
            suma = 0
            multiplicador = 2
            
            for digit in reversed(rut_number):
                suma += int(digit) * multiplicador
                multiplicador = multiplicador + 1 if multiplicador < 7 else 2
            
            resto = suma % 11
            return 'K' if resto == 1 else '0' if resto == 0 else str(11 - resto)
        except (ValueError, IndexError):
            return ""
    
    @staticmethod
    def mask_rut(rut: str, visible_chars: int = 4) -> str:
        """Ofuscar RUT mostrando solo los últimos caracteres"""
        if not rut:
            return ""
        
        clean_rut = RutValidator.clean_rut(rut)
        if len(clean_rut) <= visible_chars:
            return "*" * len(clean_rut)
        
        masked_chars = len(clean_rut) - visible_chars
        return "*" * masked_chars + clean_rut[-visible_chars:]
    
    @staticmethod
    def generate_valid_rut(base_number: int) -> str:
        """Generar un RUT válido con dígito verificador correcto"""
        if base_number < 1000000 or base_number > 99999999:
            raise ValueError("El número base debe estar entre 1,000,000 y 99,999,999")
        
        # Calcular dígito verificador
        dv = RutValidator.calculate_dv(str(base_number))
        
        # Formatear RUT
        rut = f"{base_number}{dv}"
        return RutValidator.format_rut(rut)
    
    @staticmethod
    def is_valid_format(rut: str) -> bool:
        """Verificar si el RUT tiene formato válido (sin validar DV)"""
        if not rut:
            return False
        
        clean_rut = RutValidator.clean_rut(rut)
        return bool(re.match(r'^\d{7,8}[0-9K]$', clean_rut))

# Funciones de compatibilidad para testing
def validate_rut(rut: str) -> bool:
    """Función de compatibilidad para testing"""
    return RutValidator.validate_rut(rut)

def format_rut(rut: str) -> str:
    """Función de compatibilidad para testing"""
    return RutValidator.format_rut(rut)

def clean_rut(rut: str) -> str:
    """Función de compatibilidad para testing"""
    return RutValidator.clean_rut(rut)
