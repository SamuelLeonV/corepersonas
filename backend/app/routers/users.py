from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.models.user import User
from app.schemas.common import ApiResponse
from app.services.user import UserService
from app.services.audit import AuditService
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


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario actual es admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario actual está activo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user


def validate_admin_or_self(user_id: int, current_user: User = Depends(get_current_user)) -> bool:
    """Validar que el usuario es admin o está accediendo a sus propios datos"""
    if current_user.is_admin or current_user.id == user_id:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos para acceder a este recurso"
    )

router = APIRouter()


@router.post("/", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Crear nuevo usuario (solo administradores)"""
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    try:
        # Crear usuario
        user = user_service.create_user(user_data, current_user.id)
        
        # Log adicional de auditoría
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="CREATE_USER",
            resource="users",
            resource_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Usuario creado por admin: {user.email}"
        )
        
        return ApiResponse(
            success=True,
            message="Usuario creado exitosamente",
            data={
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_active": user.is_active
            }
        )
        
    except HTTPException as e:
        # Log de error
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="CREATE_USER_FAILED",
            resource="users",
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Error al crear usuario: {str(e.detail)}"
        )
        raise e


@router.get("/", response_model=List[UserResponse])
async def get_users(
    request: Request,
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de elementos"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Obtener lista de usuarios (solo administradores)"""
    
    # Servicios
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Obtener usuarios
    users = user_service.get_users(skip=skip, limit=limit)
    
    # Log de auditoría
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="LIST_USERS",
        resource="users",
        ip_address=client_ip,
        user_agent=user_agent,
        details=f"Lista de usuarios consultada (skip: {skip}, limit: {limit})"
    )
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener usuario por ID (administradores o el propio usuario)"""
    # Validar permisos
    if not (current_user.is_admin or current_user.id == user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este recurso"
        )
    
    # Servicios
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Obtener usuario
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Log de auditoría
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="GET_USER",
        resource="users",
        resource_id=user_id,
        ip_address=client_ip,
        user_agent=user_agent,
        details=f"Usuario consultado: {user.email}"
    )
    
    return user


@router.put("/{user_id}", response_model=ApiResponse)
async def update_user(
    request: Request,
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar usuario (administradores o el propio usuario)"""
    # Validar permisos
    if not (current_user.is_admin or current_user.id == user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este recurso"
        )
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Validar permisos para cambios administrativos
    if user_data.is_admin is not None or user_data.is_active is not None:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los administradores pueden cambiar el estado de administrador o activo"
            )
    
    try:
        # Actualizar usuario
        user = user_service.update_user(user_id, user_data, current_user.id)
        
        # Log adicional de auditoría
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="UPDATE_USER",
            resource="users",
            resource_id=user_id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Usuario actualizado: {user.email}"
        )
        
        return ApiResponse(
            success=True,
            message="Usuario actualizado exitosamente",
            data={
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_active": user.is_active
            }
        )
        
    except HTTPException as e:
        # Log de error
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="UPDATE_USER_FAILED",
            resource="users",
            resource_id=user_id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Error al actualizar usuario: {str(e.detail)}"
        )
        raise e


@router.delete("/{user_id}", response_model=ApiResponse)
async def delete_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Eliminar usuario (solo administradores)"""
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Validar que no se elimine a sí mismo
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    try:
        # Eliminar usuario
        success = user_service.delete_user(user_id, current_user.id)
        
        if success:
            # Log adicional de auditoría
            audit_service.create_audit_log(
                user_id=current_user.id,
                action="DELETE_USER",
                resource="users",
                resource_id=user_id,
                ip_address=client_ip,
                user_agent=user_agent,
                details=f"Usuario eliminado con ID: {user_id}"
            )
            
            return ApiResponse(
                success=True,
                message="Usuario eliminado exitosamente"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar usuario"
            )
            
    except HTTPException as e:
        # Log de error
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="DELETE_USER_FAILED",
            resource="users",
            resource_id=user_id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Error al eliminar usuario: {str(e.detail)}"
        )
        raise e
