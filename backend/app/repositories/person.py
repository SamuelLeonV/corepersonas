"""
Repositorio para operaciones de personas.
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate
from app.repositories.base import BaseRepository


class PersonRepository(BaseRepository[Person, PersonCreate, PersonUpdate]):
    """Repositorio para operaciones de personas"""
    
    def __init__(self, db: Session):
        super().__init__(Person, db)
    
    def get_by_rut_hash(self, rut_hash: str) -> Optional[Person]:
        """Obtener persona por hash de RUT"""
        return self.db.query(Person).filter(Person.rut_hash == rut_hash).first()
    
    def search_by_name(self, nombre: str = None, apellido: str = None, skip: int = 0, limit: int = 100) -> List[Person]:
        """Buscar personas por nombre y/o apellido"""
        query = self.db.query(Person)
        
        if nombre:
            query = query.filter(Person.nombre.ilike(f"%{nombre}%"))
        if apellido:
            query = query.filter(Person.apellido.ilike(f"%{apellido}%"))
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_created_by(self, created_by: int, skip: int = 0, limit: int = 100) -> List[Person]:
        """Obtener personas creadas por un usuario específico"""
        return self.db.query(Person).filter(Person.created_by == created_by).offset(skip).limit(limit).all()
    
    def create_person(self, person_data: PersonCreate, created_by: int) -> Person:
        """Crear nueva persona"""
        # Importar el servicio de seguridad
        from app.core.security_service import SecurityService
        
        # Encriptar el RUT antes de almacenarlo
        encrypted_rut = SecurityService.encrypt_rut(person_data.rut)
        
        db_person = Person(
            rut=encrypted_rut,  # Usar RUT encriptado
            nombre=person_data.nombre,
            apellido=person_data.apellido,
            email=person_data.email,
            telefono=person_data.telefono,
            direccion=person_data.direccion,
            fecha_nacimiento=person_data.fecha_nacimiento,
            created_by=created_by
        )
        
        # Generar hashes (usar RUT original sin encriptar para el hash)
        db_person.set_rut_hash(person_data.rut)
        db_person.set_religion_hash(person_data.religion)
        
        self.db.add(db_person)
        self.db.commit()
        self.db.refresh(db_person)
        return db_person
    
    def update_person(self, db_person: Person, person_data: PersonUpdate) -> Person:
        """Actualizar persona existente"""
        # Importar el servicio de seguridad
        from app.core.security_service import SecurityService
        
        update_data = person_data.dict(exclude_unset=True)
        
        # Actualizar campos básicos
        for field, value in update_data.items():
            if field not in ['rut', 'religion']:
                setattr(db_person, field, value)
        
        # Actualizar RUT si se proporciona
        if 'rut' in update_data:
            # Encriptar el nuevo RUT
            encrypted_rut = SecurityService.encrypt_rut(update_data['rut'])
            db_person.rut = encrypted_rut
            # Generar nuevo hash usando el RUT original
            db_person.set_rut_hash(update_data['rut'])
        
        # Actualizar religión si se proporciona
        if 'religion' in update_data:
            db_person.set_religion_hash(update_data['religion'])
        
        self.db.commit()
        self.db.refresh(db_person)
        return db_person
    
    def count_by_created_by(self, created_by: int) -> int:
        """Contar personas creadas por un usuario específico"""
        return self.db.query(Person).filter(Person.created_by == created_by).count()
