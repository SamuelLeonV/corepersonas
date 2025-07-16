"""
Utilidades del sistema de auditoría
"""

from .rut import RutValidator
from .religion import ReligionHasher  
from .responses import ResponseUtils
from .system_status import (
    get_system_status,
    print_system_status
)
from .testing import APITester
from .populate_db import (
    populate_database,
    clear_test_data
)

# Alias para mantener compatibilidad
validate_rut = RutValidator.validate_rut
format_rut = RutValidator.format_rut
generate_valid_rut = RutValidator.generate_valid_rut
clean_rut = RutValidator.clean_rut
mask_rut = RutValidator.mask_rut

hash_religion = ReligionHasher.hash_religion
verify_religion = ReligionHasher.verify_religion

create_success_response = ResponseUtils.success_response
create_error_response = ResponseUtils.error_response
create_paginated_response = ResponseUtils.paginated_response

__all__ = [
    # Classes
    "RutValidator",
    "ReligionHasher", 
    "ResponseUtils",
    "APITester",
    # Functions
    "validate_rut",
    "format_rut", 
    "generate_valid_rut",
    "clean_rut",
    "mask_rut",
    "hash_religion",
    "verify_religion",
    "create_success_response",
    "create_error_response",
    "create_paginated_response",
    "get_system_status",
    "print_system_status",
    "populate_database",
    "clear_test_data"
]
