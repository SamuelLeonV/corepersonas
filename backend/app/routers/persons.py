from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
import math

from app.db.database import get_db
from app.schemas.person import PersonCreate, PersonUpdate, PersonResponse
from app.schemas.user import UserResponse
from app.models.user import User
from app.schemas.common import ApiResponse, PaginatedResponse
from app.services.person import PersonService
from app.services.audit import AuditService
from app.core.security_service import SecurityService
from app.deps.auth import get_current_user


def get_client_ip(request: Request) -> str:
    """Obtener la IP del cliente"""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """Obtener el User-Agent del cliente"""
    return request.headers.get("User-Agent", "unknown")


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario actual está activo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario actual es admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user


router = APIRouter()


@router.post(
    "/", 
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva persona",
    description="Crear un nuevo registro de persona con validación de RUT chileno y hash de religión",
    responses={
        201: {
            "description": "Persona creada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Persona creada exitosamente",
                        "data": {
                            "id": 1,
                            "rut": "****7890-1",
                            "nombre": "Juan",
                            "apellido": "Pérez",
                            "religion_indicator": "a1b2c3d4",
                            "email": "juan@ejemplo.com",
                            "telefono": "+56912345678",
                            "direccion": "Calle Falsa 123",
                            "fecha_nacimiento": "1990-05-15",
                            "created_at": "2025-07-12T21:00:00Z",
                            "updated_at": "2025-07-12T21:00:00Z"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Error en los datos de entrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "RUT inválido o ya existe"
                    }
                }
            }
        },
        401: {
            "description": "No autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se pudo validar las credenciales"
                    }
                }
            }
        },
        422: {
            "description": "Error de validación",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "rut"],
                                "msg": "RUT chileno inválido",
                                "type": "value_error"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def create_person(
    request: Request,
    person_data: PersonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear un nuevo registro de persona.
    
    - **rut**: RUT chileno válido con formato XX.XXX.XXX-X o XXXXXXXX-X
    - **nombre**: Nombre de la persona (obligatorio)
    - **apellido**: Apellido de la persona (obligatorio)
    - **religion**: Religión de la persona (se hashea de forma irreversible)
    - **email**: Email opcional de la persona
    - **telefono**: Teléfono opcional
    - **direccion**: Dirección opcional
    - **fecha_nacimiento**: Fecha de nacimiento opcional
    
    **Características de seguridad:**
    - RUT se almacena completo pero se muestra ofuscado
    - Religión se hashea con SHA256 + salt
    - Validación completa de RUT chileno
    - Logging de auditoría automático
    """
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    person_service = PersonService(db)
    audit_service = AuditService(db)
    
    try:
        # Crear persona
        person = person_service.create_person(person_data, current_user.id)
        
        # Log adicional de auditoría
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="CREATE_PERSON",
            resource="persons",
            resource_id=person.id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Persona creada: {person.nombre} {person.apellido}"
        )
        
        return ApiResponse(
            success=True,
            message="Persona creada exitosamente",
            data={
                "id": person.id,
                "nombre": person.nombre,
                "apellido": person.apellido
            }
        )
        
    except HTTPException as e:
        # Log de error
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="CREATE_PERSON_FAILED",
            resource="persons",
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Error al crear persona: {str(e.detail)}"
        )
        raise e


@router.get("/", response_model=PaginatedResponse)
async def get_persons(
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    search: Optional[str] = Query(None, description="Término de búsqueda"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener lista de personas con paginación y búsqueda"""
    
    # Calcular offset
    skip = (page - 1) * per_page
    
    # Servicios
    person_service = PersonService(db)
    audit_service = AuditService(db)
    
    # Obtener personas
    persons, total = person_service.get_persons(
        skip=skip,
        limit=per_page,
        search=search,
        requested_by=current_user.id
    )
    
    # Debug: Verificar tipo de datos
    print(f"🔍 DEBUG: persons type: {type(persons)}")
    print(f"🔍 DEBUG: persons length: {len(persons)}")
    if persons:
        print(f"🔍 DEBUG: first person type: {type(persons[0])}")
        print(f"🔍 DEBUG: first person has dict: {hasattr(persons[0], 'dict')}")
    
    # Calcular metadatos de paginación
    pages = math.ceil(total / per_page)
    has_next = page < pages
    has_prev = page > 1
    
    # Log de auditoría
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="LIST_PERSONS",
        resource="persons",
        ip_address=client_ip,
        user_agent=user_agent,
        details=f"Lista de personas consultada (página: {page}, por_página: {per_page}, búsqueda: {search})"
    )
    
    # Procesar items de forma segura
    items = []
    for person in persons:
        if hasattr(person, 'dict'):
            items.append(person.dict())
        else:
            # Si no tiene dict, puede ser que ya sea un dict
            items.append(person)
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        has_next=has_next,
        has_prev=has_prev
    )


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(
    request: Request,
    person_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener persona por ID"""
    
    # Servicios
    person_service = PersonService(db)
    audit_service = AuditService(db)
    
    # Obtener persona
    person = person_service.get_person_by_id(person_id, current_user.id)
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )
    
    # Log de auditoría
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="GET_PERSON",
        resource="persons",
        resource_id=person_id,
        ip_address=client_ip,
        user_agent=user_agent,
        details=f"Persona consultada: {person.nombre} {person.apellido}"
    )
    
    # El PersonDetailResponse ya viene con todos los datos procesados, 
    # incluyendo religion_indicator y RUT desencriptado
    return PersonResponse(
        id=person.id,
        rut=person.rut,  # Ya viene desencriptado del servicio
        rut_masked=person.rut_masked,  # Ya viene procesado del servicio
        nombre=person.nombre,
        apellido=person.apellido,
        religion_indicator=person.religion_indicator,  # Ya viene procesado del servicio
        email=person.email,
        telefono=person.telefono,
        direccion=person.direccion,
        fecha_nacimiento=person.fecha_nacimiento,
        created_at=person.created_at,
        updated_at=person.updated_at
    )


@router.put("/{person_id}", response_model=ApiResponse)
async def update_person(
    request: Request,
    person_id: int,
    person_data: PersonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar persona"""
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    person_service = PersonService(db)
    audit_service = AuditService(db)
    
    try:
        # Actualizar persona
        person = person_service.update_person(person_id, person_data, current_user.id)
        
        # Log adicional de auditoría
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="UPDATE_PERSON",
            resource="persons",
            resource_id=person_id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Persona actualizada: {person.nombre} {person.apellido}"
        )
        
        return ApiResponse(
            success=True,
            message="Persona actualizada exitosamente",
            data={
                "id": person.id,
                "nombre": person.nombre,
                "apellido": person.apellido
            }
        )
        
    except HTTPException as e:
        # Log de error
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="UPDATE_PERSON_FAILED",
            resource="persons",
            resource_id=person_id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Error al actualizar persona: {str(e.detail)}"
        )
        raise e


@router.delete("/{person_id}", response_model=ApiResponse)
async def delete_person(
    request: Request,
    person_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar persona"""
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    person_service = PersonService(db)
    audit_service = AuditService(db)
    
    try:
        # Eliminar persona
        success = person_service.delete_person(person_id, current_user.id)
        
        if success:
            # Log adicional de auditoría
            audit_service.create_audit_log(
                user_id=current_user.id,
                action="DELETE_PERSON",
                resource="persons",
                resource_id=person_id,
                ip_address=client_ip,
                user_agent=user_agent,
                details=f"Persona eliminada con ID: {person_id}"
            )
            
            return ApiResponse(
                success=True,
                message="Persona eliminada exitosamente"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar persona"
            )
            
    except HTTPException as e:
        # Log de error
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="DELETE_PERSON_FAILED",
            resource="persons",
            resource_id=person_id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Error al eliminar persona: {str(e.detail)}"
        )
        raise e


@router.get(
    "/search/rut", 
    response_model=PersonResponse,
    summary="Buscar persona por RUT",
    description="Buscar una persona específica usando su RUT chileno",
    responses={
        200: {
            "description": "Persona encontrada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "rut": "****7890-1",
                        "nombre": "Juan",
                        "apellido": "Pérez",
                        "religion_indicator": "a1b2c3d4",
                        "email": "juan@ejemplo.com",
                        "telefono": "+56912345678",
                        "direccion": "Calle Falsa 123",
                        "fecha_nacimiento": "1990-05-15",
                        "created_at": "2025-07-12T21:00:00Z",
                        "updated_at": "2025-07-12T21:00:00Z"
                    }
                }
            }
        },
        404: {
            "description": "Persona no encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Persona no encontrada"
                    }
                }
            }
        },
        401: {
            "description": "No autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se pudo validar las credenciales"
                    }
                }
            }
        },
        422: {
            "description": "RUT inválido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["query", "rut"],
                                "msg": "RUT chileno inválido",
                                "type": "value_error"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def search_person_by_rut(
    request: Request,
    rut: str = Query(..., description="RUT de la persona a buscar (formato: XX.XXX.XXX-X o XXXXXXXX-X)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Buscar una persona específica por su RUT chileno.
    
    - **rut**: RUT chileno válido con formato XX.XXX.XXX-X o XXXXXXXX-X
    
    **Características de seguridad:**
    - RUT se valida completamente antes de la búsqueda
    - Búsqueda por hash para mayor seguridad
    - RUT se muestra ofuscado en la respuesta
    - Logging de auditoría automático
    - Requiere autenticación
    """
    
    # Servicios
    person_service = PersonService(db)
    audit_service = AuditService(db)
    
    # Buscar persona
    person = person_service.search_by_rut(rut, current_user.id)
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )
    
    # Log de auditoría
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="SEARCH_PERSON_BY_RUT",
        resource="persons",
        resource_id=person.id,
        ip_address=client_ip,
        user_agent=user_agent,
        details=f"Búsqueda por RUT realizada"
    )
    
    return person
