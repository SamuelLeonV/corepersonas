"""
Servicio para operaciones de personas.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate, PersonResponse, PersonDetailResponse
from app.repositories.person import PersonRepository
from app.repositories.audit import AuditRepository
import logging
from app.repositories.audit import AuditRepository
from app.core.config import settings
import hashlib


class PersonService:
    """Servicio para operaciones de personas"""
    
    def __init__(self, db: Session):
        self.db = db
        self.person_repo = PersonRepository(db)
        self.audit_repo = AuditRepository(db)
    
    def _mask_rut(self, rut: str) -> str:
        """Ofuscar RUT para mostrar"""
        if not rut:
            return ""
        
        clean_rut = rut.replace(".", "").replace("-", "")
        if len(clean_rut) <= settings.RUT_MASK_LENGTH:
            return "*" * len(clean_rut)
        
        visible_chars = settings.RUT_MASK_LENGTH
        masked_chars = len(clean_rut) - visible_chars
        
        return "*" * masked_chars + clean_rut[-visible_chars:]
    
    def _get_religion_indicator(self, religion_hash: str) -> str:
        """Obtener indicador de religión desde hash"""
        if not religion_hash:
            return "no_especificada"
        
        # Usar primeros 8 caracteres del hash como indicador
        return f"hash_{religion_hash[:8]}"
    
    def get_persons(self, skip: int = 0, limit: int = 100, search: str = None, user_id: int = None, ip_address: str = None, requested_by: int = None):
        """Obtener lista de personas con búsqueda opcional"""
        
        # Obtener personas usando repositorio
        if search:
            # Búsqueda simple - se puede mejorar en el futuro
            persons = self.person_repo.get_multi(skip=skip, limit=limit)
            # Filtrar por nombre o apellido si se proporciona búsqueda
            filtered_persons = []
            for person in persons:
                if (search.lower() in person.nombre.lower() or 
                    search.lower() in person.apellido.lower() or
                    search.lower() in (person.email or "").lower()):
                    filtered_persons.append(person)
            persons = filtered_persons[:limit]  # Aplicar límite después del filtro
            total = len(filtered_persons)
        else:
            persons = self.person_repo.get_multi(skip=skip, limit=limit)
            # Para obtener el total, hacemos una consulta adicional
            total = self.person_repo.count()
        
        # Log de consulta masiva
        user_id_to_log = user_id or requested_by
        if user_id_to_log:
            self.audit_repo.create_log(
                user_id=user_id_to_log,
                action="READ",
                resource="persons",
                ip_address=ip_address,
                details=f"Consulta masiva de personas: {len(persons)} registros"
            )
        
        # Importar servicio de seguridad para desencriptar RUT
        from app.security import SecurityService
        
        # Convertir a esquema de respuesta
        result = []
        for person in persons:
            # Desencriptar el RUT antes de crear la respuesta
            try:
                decrypted_rut = SecurityService.decrypt_rut(person.rut)
                
                # Verificar si la desencriptación fue exitosa
                if decrypted_rut in ["RUT_DECRYPT_ERROR", "RUT_CORRUPTED"]:
                    formatted_rut = f"ERROR_ID_{person.id}"
                    clean_rut = "ERROR"
                    logging.warning(f"RUT corrupto para persona {person.id}")
                else:
                    # Limpiar el RUT desencriptado antes de formatear
                    clean_rut = SecurityService.clean_rut(decrypted_rut)
                    # Solo formatear si el RUT limpio es válido
                    if clean_rut and SecurityService.validate_rut(clean_rut):
                        formatted_rut = SecurityService.format_rut(clean_rut)
                    else:
                        # Si no es válido, usar el RUT limpio sin formatear
                        formatted_rut = clean_rut if clean_rut else f"INVALID_ID_{person.id}"
                        
            except Exception as e:
                # Si ocurre un error, registrarlo y usar un RUT por defecto
                logging.error(f"Error al procesar RUT para persona {person.id}: {str(e)}")
                decrypted_rut = "ERROR_DECRYPT"
                formatted_rut = f"ERROR_ID_{person.id}"
                clean_rut = "ERROR"
            
            # Crear respuesta con RUT desencriptado
            person_dict = {
                'id': person.id,
                'rut': formatted_rut,  # RUT desencriptado y formateado
                'rut_masked': SecurityService.mask_rut(clean_rut) if clean_rut not in ["ERROR", "ERROR_DECRYPT"] else "ERROR",
                'nombre': person.nombre,
                'apellido': person.apellido,
                'religion_indicator': self._get_religion_indicator(person.religion_hash),
                'email': person.email,
                'telefono': person.telefono,
                'direccion': person.direccion,
                'fecha_nacimiento': person.fecha_nacimiento,
                'created_at': person.created_at,
                'updated_at': person.updated_at
            }
            
            person_response = PersonResponse(**person_dict)
            result.append(person_response)
        
        return result, total
    
    def get_person_by_id(self, person_id: int, user_id: int = None, ip_address: str = None) -> Optional[PersonDetailResponse]:
        """Obtener persona por ID"""
        person = self.person_repo.get(person_id)
        if not person:
            return None
        
        # Log de consulta individual
        self.audit_repo.create_log(
            user_id=user_id,
            action="READ",
            resource="persons",
            resource_id=person.id,
            ip_address=ip_address,
            details=f"Consulta de persona: {person.nombre} {person.apellido}"
        )
        
        # Importar servicio de seguridad para desencriptar RUT
        from app.security import SecurityService
        
        # Desencriptar el RUT
        try:
            decrypted_rut = SecurityService.decrypt_rut(person.rut)
            formatted_rut = SecurityService.format_rut(decrypted_rut)
        except Exception as e:
            # Si ocurre un error, registrarlo y usar el RUT encriptado
            logging.error(f"Error al desencriptar RUT: {str(e)}")
            decrypted_rut = person.rut
            formatted_rut = person.rut
        
        # Crear respuesta con RUT desencriptado
        person_dict = {
            'id': person.id,
            'rut': formatted_rut,  # RUT desencriptado y formateado
            'rut_masked': self._mask_rut(decrypted_rut),  # RUT ofuscado
            'nombre': person.nombre,
            'apellido': person.apellido,
            'religion_indicator': self._get_religion_indicator(person.religion_hash),
            'email': person.email,
            'telefono': person.telefono,
            'direccion': person.direccion,
            'fecha_nacimiento': person.fecha_nacimiento,
            'created_at': person.created_at,
            'updated_at': person.updated_at
        }
        
        person_response = PersonDetailResponse(**person_dict)
        
        return person_response
    
    def search_person_by_rut(self, rut: str, user_id: int = None, ip_address: str = None) -> Optional[PersonDetailResponse]:
        """Buscar persona por RUT"""
        # Generar hash del RUT para búsqueda
        clean_rut = rut.replace(".", "").replace("-", "").lower()
        rut_hash = hashlib.sha256(clean_rut.encode()).hexdigest()
        
        person = self.person_repo.get_by_rut_hash(rut_hash)
        if not person:
            # Log de búsqueda fallida
            self.audit_repo.create_log(
                user_id=user_id,
                action="SEARCH_FAILED",
                resource="persons",
                ip_address=ip_address,
                details=f"Búsqueda fallida por RUT: {self._mask_rut(rut)}"
            )
            return None
        
        # Log de búsqueda exitosa
        self.audit_repo.create_log(
            user_id=user_id,
            action="SEARCH_SUCCESS",
            resource="persons",
            resource_id=person.id,
            ip_address=ip_address,
            details=f"Búsqueda exitosa por RUT: {person.nombre} {person.apellido}"
        )
        
        # Importar servicio de seguridad para desencriptar RUT
        from app.security import SecurityService
        
        # Desencriptar el RUT
        try:
            decrypted_rut = SecurityService.decrypt_rut(person.rut)
            formatted_rut = SecurityService.format_rut(decrypted_rut)
        except Exception as e:
            # Si ocurre un error, registrarlo y usar el RUT encriptado
            logging.error(f"Error al desencriptar RUT: {str(e)}")
            decrypted_rut = person.rut
            formatted_rut = person.rut
        
        # Crear respuesta con RUT desencriptado
        person_dict = {
            'id': person.id,
            'rut': formatted_rut,  # RUT desencriptado y formateado
            'rut_masked': self._mask_rut(decrypted_rut),  # RUT ofuscado
            'nombre': person.nombre,
            'apellido': person.apellido,
            'religion_indicator': self._get_religion_indicator(person.religion_hash),
            'email': person.email,
            'telefono': person.telefono,
            'direccion': person.direccion,
            'fecha_nacimiento': person.fecha_nacimiento,
            'created_at': person.created_at,
            'updated_at': person.updated_at
        }
        
        person_response = PersonDetailResponse(**person_dict)
        
        return person_response
    
    def create_person(self, person_data: PersonCreate, created_by: int, ip_address: str = None) -> PersonResponse:
        """Crear nueva persona"""
        # Verificar si el RUT ya existe
        clean_rut = person_data.rut.replace(".", "").replace("-", "").lower()
        rut_hash = hashlib.sha256(clean_rut.encode()).hexdigest()
        
        if self.person_repo.get_by_rut_hash(rut_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El RUT ya está registrado"
            )
        
        # Crear persona
        person = self.person_repo.create_person(person_data, created_by)
        
        # Log de creación
        self.audit_repo.create_log(
            user_id=created_by,
            action="CREATE",
            resource="persons",
            resource_id=person.id,
            ip_address=ip_address,
            details=f"Persona creada: {person.nombre} {person.apellido}"
        )
        
        # Importar servicio de seguridad para desencriptar RUT
        from app.security import SecurityService
        
        # Desencriptar el RUT
        try:
            decrypted_rut = SecurityService.decrypt_rut(person.rut)
            formatted_rut = SecurityService.format_rut(decrypted_rut)
        except Exception as e:
            # Si ocurre un error, registrarlo y usar el RUT encriptado
            logging.error(f"Error al desencriptar RUT: {str(e)}")
            decrypted_rut = person.rut
            formatted_rut = person.rut
        
        # Crear respuesta con RUT desencriptado
        person_dict = {
            'id': person.id,
            'rut': formatted_rut,  # RUT desencriptado y formateado
            'rut_masked': self._mask_rut(decrypted_rut),  # RUT ofuscado
            'nombre': person.nombre,
            'apellido': person.apellido,
            'religion_indicator': self._get_religion_indicator(person.religion_hash),
            'email': person.email,
            'telefono': person.telefono,
            'direccion': person.direccion,
            'fecha_nacimiento': person.fecha_nacimiento,
            'created_at': person.created_at,
            'updated_at': person.updated_at
        }
        
        person_response = PersonResponse(**person_dict)
        
        return person_response
    
    def update_person(self, person_id: int, person_data: PersonUpdate, updated_by: int, ip_address: str = None) -> PersonResponse:
        """Actualizar persona"""
        person = self.person_repo.get(person_id)
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada"
            )
        
        # Verificar si el nuevo RUT ya existe
        if person_data.rut:
            clean_rut = person_data.rut.replace(".", "").replace("-", "").lower()
            rut_hash = hashlib.sha256(clean_rut.encode()).hexdigest()
            
            existing_person = self.person_repo.get_by_rut_hash(rut_hash)
            if existing_person and existing_person.id != person_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El RUT ya está registrado"
                )
        
        # Actualizar persona
        updated_person = self.person_repo.update_person(person, person_data)
        
        # Log de actualización
        self.audit_repo.create_log(
            user_id=updated_by,
            action="UPDATE",
            resource="persons",
            resource_id=person.id,
            ip_address=ip_address,
            details=f"Persona actualizada: {person.nombre} {person.apellido}"
        )
        
        # Importar servicio de seguridad para desencriptar RUT
        from app.security import SecurityService
        
        # Convertir a esquema de respuesta
        person_response = PersonResponse.model_validate(updated_person)
        
        # Desencriptar el RUT
        try:
            decrypted_rut = SecurityService.decrypt_rut(updated_person.rut)
            person_response.rut = decrypted_rut  # Usar el RUT desencriptado
        except Exception as e:
            # Si ocurre un error, registrarlo y mantener el RUT encriptado
            logging.error(f"Error al desencriptar RUT: {str(e)}")
            
        person_response.rut_masked = self._mask_rut(updated_person.rut)
        person_response.religion_indicator = self._get_religion_indicator(updated_person.religion_hash)
        
        return person_response
    
    def delete_person(self, person_id: int, deleted_by: int, ip_address: str = None) -> bool:
        """Eliminar persona"""
        person = self.person_repo.get(person_id)
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada"
            )
        
        # Log de eliminación
        self.audit_repo.create_log(
            user_id=deleted_by,
            action="DELETE",
            resource="persons",
            resource_id=person.id,
            ip_address=ip_address,
            details=f"Persona eliminada: {person.nombre} {person.apellido}"
        )
        
        # Eliminar persona
        self.person_repo.delete(person_id)
        return True
    
    def search_persons_by_name(self, nombre: str = None, apellido: str = None, 
                              skip: int = 0, limit: int = 100, 
                              user_id: int = None, ip_address: str = None) -> List[PersonResponse]:
        """Buscar personas por nombre y/o apellido"""
        persons = self.person_repo.search_by_name(nombre, apellido, skip, limit)
        
        # Log de búsqueda
        search_criteria = []
        if nombre:
            search_criteria.append(f"nombre: {nombre}")
        if apellido:
            search_criteria.append(f"apellido: {apellido}")
        
        self.audit_repo.create_log(
            user_id=user_id,
            action="SEARCH",
            resource="persons",
            ip_address=ip_address,
            details=f"Búsqueda por {', '.join(search_criteria)}: {len(persons)} resultados"
        )
        
        # Importar servicio de seguridad para desencriptar RUT
        from app.security import SecurityService
        
        # Convertir a esquema de respuesta
        result = []
        for person in persons:
            person_response = PersonResponse.model_validate(person)
            
            # Desencriptar el RUT
            try:
                decrypted_rut = SecurityService.decrypt_rut(person.rut)
                person_response.rut = decrypted_rut  # Usar el RUT desencriptado
            except Exception as e:
                # Si ocurre un error, registrarlo y mantener el RUT encriptado
                logging.error(f"Error al desencriptar RUT: {str(e)}")
                
            person_response.rut_masked = self._mask_rut(person.rut)
            person_response.religion_indicator = self._get_religion_indicator(person.religion_hash)
            result.append(person_response)
        
        return result
    
    def get_persons_by_user(self, created_by: int, skip: int = 0, limit: int = 100, 
                           user_id: int = None, ip_address: str = None) -> List[PersonResponse]:
        """Obtener personas creadas por un usuario específico"""
        persons = self.person_repo.get_by_created_by(created_by, skip, limit)
        
        # Log de consulta
        self.audit_repo.create_log(
            user_id=user_id,
            action="READ",
            resource="persons",
            ip_address=ip_address,
            details=f"Consulta de personas creadas por usuario {created_by}: {len(persons)} registros"
        )
        
        # Importar servicio de seguridad para desencriptar RUT
        from app.security import SecurityService
        
        # Convertir a esquema de respuesta
        result = []
        for person in persons:
            person_response = PersonResponse.model_validate(person)
            
            # Desencriptar el RUT
            try:
                decrypted_rut = SecurityService.decrypt_rut(person.rut)
                person_response.rut = decrypted_rut  # Usar el RUT desencriptado
            except Exception as e:
                # Si ocurre un error, registrarlo y mantener el RUT encriptado
                logging.error(f"Error al desencriptar RUT: {str(e)}")
                
            person_response.rut_masked = self._mask_rut(person.rut)
            person_response.religion_indicator = self._get_religion_indicator(person.religion_hash)
            result.append(person_response)
        
        return result
