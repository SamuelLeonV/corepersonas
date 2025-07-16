"""
Rutas de la API para usuarios.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import ApiResponse, PaginatedResponse
from app.services.user import UserService
from app.deps.auth import get_current_user, get_current_admin_user, get_client_ip
from app.models.user import User
from app.utils.responses import ResponseUtils

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse,
    summary="Listar usuarios",
    description="Obtener lista paginada de usuarios. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def get_users(
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de usuarios"""
    user_service = UserService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    users = user_service.get_users(skip=skip, limit=limit)
    
    # Contar total de usuarios
    from app.repositories.user import UserRepository
    user_repo = UserRepository(db)
    total = user_repo.count()
    
    return ResponseUtils.paginated_response(
        items=[user.dict() for user in users],
        total=total,
        page=page,
        per_page=per_page
    )


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crear nuevo usuario. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def create_user(
    request: Request,
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Crear nuevo usuario"""
    user_service = UserService(db)
    ip_address = get_client_ip(request)
    
    return user_service.create_user(user_data, current_user.id, ip_address)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario",
    description="Obtener usuario por ID. Administradores pueden ver cualquier usuario, usuarios normales solo a sí mismos."
)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener usuario por ID"""
    # Verificar permisos
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este usuario"
        )
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualizar usuario. Administradores pueden actualizar cualquier usuario, usuarios normales solo a sí mismos."
)
async def update_user(
    user_id: int,
    request: Request,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar usuario"""
    # Verificar permisos
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este usuario"
        )
    
    # Solo administradores pueden cambiar is_admin
    if not current_user.is_admin and user_data.is_admin is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para cambiar permisos de administrador"
        )
    
    user_service = UserService(db)
    ip_address = get_client_ip(request)
    
    return user_service.update_user(user_id, user_data, current_user.id, ip_address)


@router.delete(
    "/{user_id}",
    response_model=ApiResponse,
    summary="Eliminar usuario",
    description="Eliminar usuario. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def delete_user(
    user_id: int,
    request: Request,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Eliminar usuario"""
    # No permitir auto-eliminación
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    user_service = UserService(db)
    ip_address = get_client_ip(request)
    
    success = user_service.delete_user(user_id, current_user.id, ip_address)
    
    if success:
        return ResponseUtils.success_response("Usuario eliminado exitosamente")
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar usuario"
        )
