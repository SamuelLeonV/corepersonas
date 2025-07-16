"""
Rutas de la API para personas.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.person import PersonCreate, PersonUpdate, PersonResponse, PersonDetailResponse
from app.schemas.common import ApiResponse, PaginatedResponse
from app.services.person import PersonService
from app.deps.auth import get_current_user, get_client_ip
from app.models.user import User
from app.utils.responses import ResponseUtils

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse,
    summary="Listar personas",
    description="Obtener lista paginada de personas con RUT desencriptado."
)
async def get_persons(
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de personas"""
    person_service = PersonService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    persons = person_service.get_persons(skip=skip, limit=limit, user_id=current_user.id, ip_address=ip_address)
    
    # Contar total de personas
    from app.repositories.person import PersonRepository
    person_repo = PersonRepository(db)
    total = person_repo.count()
    
    # Convertir cada persona a diccionario de manera segura
    items = []
    for person in persons:
        if hasattr(person, 'dict'):
            # Si es un objeto Pydantic con método dict()
            items.append(person.dict())
        elif hasattr(person, 'model_dump'):
            # Si es un objeto Pydantic v2 con método model_dump()
            items.append(person.model_dump())
        else:
            # Si ya es un diccionario o tiene otra estructura
            items.append(person)
    
    return ResponseUtils.paginated_response(
        items=items,
        total=total,
        page=page,
        per_page=per_page
    )


@router.post(
    "/",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear persona",
    description="Crear nueva persona con validación de RUT chileno, hash de religión y devolver RUT desencriptado."
)
async def create_person(
    request: Request,
    person_data: PersonCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear nueva persona"""
    person_service = PersonService(db)
    ip_address = get_client_ip(request)
    
    return person_service.create_person(person_data, current_user.id, ip_address)


@router.get(
    "/{person_id}",
    response_model=PersonDetailResponse,
    summary="Obtener persona",
    description="Obtener persona por ID con información detallada y RUT desencriptado."
)
async def get_person(
    person_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener persona por ID"""
    person_service = PersonService(db)
    ip_address = get_client_ip(request)
    
    person = person_service.get_person_by_id(person_id, current_user.id, ip_address)
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )
    
    return person


@router.put(
    "/{person_id}",
    response_model=PersonResponse,
    summary="Actualizar persona",
    description="Actualizar datos de persona existente y devolver RUT desencriptado."
)
async def update_person(
    person_id: int,
    request: Request,
    person_data: PersonUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar persona"""
    person_service = PersonService(db)
    ip_address = get_client_ip(request)
    
    return person_service.update_person(person_id, person_data, current_user.id, ip_address)


@router.delete(
    "/{person_id}",
    response_model=ApiResponse,
    summary="Eliminar persona",
    description="Eliminar persona del sistema."
)
async def delete_person(
    person_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar persona"""
    person_service = PersonService(db)
    ip_address = get_client_ip(request)
    
    success = person_service.delete_person(person_id, current_user.id, ip_address)
    
    if success:
        return ResponseUtils.success_response("Persona eliminada exitosamente")
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar persona"
        )


@router.get(
    "/search/rut",
    response_model=PersonDetailResponse,
    summary="Buscar por RUT",
    description="Buscar persona por RUT chileno y devolver información con RUT desencriptado."
)
async def search_person_by_rut(
    rut: str = Query(..., description="RUT chileno a buscar"),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buscar persona por RUT"""
    person_service = PersonService(db)
    ip_address = get_client_ip(request)
    
    person = person_service.search_person_by_rut(rut, current_user.id, ip_address)
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada con el RUT proporcionado"
        )
    
    return person


@router.get(
    "/search/name",
    response_model=PaginatedResponse,
    summary="Buscar por nombre",
    description="Buscar personas por nombre y/o apellido con RUT desencriptado."
)
async def search_persons_by_name(
    request: Request,
    nombre: Optional[str] = Query(None, description="Nombre a buscar"),
    apellido: Optional[str] = Query(None, description="Apellido a buscar"),
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buscar personas por nombre y/o apellido"""
    if not nombre and not apellido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un nombre o apellido para la búsqueda"
        )
    
    person_service = PersonService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    persons = person_service.search_persons_by_name(
        nombre=nombre, 
        apellido=apellido, 
        skip=skip, 
        limit=limit, 
        user_id=current_user.id, 
        ip_address=ip_address
    )
    
    # Para el total, necesitamos hacer la consulta sin paginación
    from app.repositories.person import PersonRepository
    person_repo = PersonRepository(db)
    total_persons = person_repo.search_by_name(nombre, apellido, skip=0, limit=10000)
    total = len(total_persons)
    
    return ResponseUtils.paginated_response(
        items=[person.dict() for person in persons],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get(
    "/my-persons",
    response_model=PaginatedResponse,
    summary="Mis personas",
    description="Obtener personas creadas por el usuario actual."
)
async def get_my_persons(
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener personas creadas por el usuario actual"""
    person_service = PersonService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    persons = person_service.get_persons_by_user(
        created_by=current_user.id,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        ip_address=ip_address
    )
    
    # Contar total de personas creadas por el usuario
    from app.repositories.person import PersonRepository
    person_repo = PersonRepository(db)
    total = person_repo.count_by_created_by(current_user.id)
    
    return ResponseUtils.paginated_response(
        items=[person.dict() for person in persons],
        total=total,
        page=page,
        per_page=per_page
    )
