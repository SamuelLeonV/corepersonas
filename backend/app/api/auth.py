"""
Rutas de la API para autenticación.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import Token, LoginRequest, UserCreate, UserResponse
from app.schemas.common import ApiResponse
from app.services.auth import AuthService
from app.deps.auth import get_current_user, get_client_ip, get_user_agent
from app.models.user import User

router = APIRouter()


@router.post(
    "/login", 
    response_model=Token,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña. Retorna un token JWT válido por 30 minutos.",
    responses={
        200: {
            "description": "Login exitoso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Credenciales inválidas",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email o contraseña incorrectos"
                    }
                }
            }
        }
    }
)
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Iniciar sesión de usuario"""
    auth_service = AuthService(db)
    
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    try:
        token = auth_service.login(
            email=login_data.email,
            password=login_data.password,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )


@router.post(
    "/register",
    response_model=Token,
    summary="Registrar usuario",
    description="Crear nueva cuenta de usuario. Solo usuarios normales, no administradores.",
    responses={
        201: {
            "description": "Usuario registrado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Email ya registrado o datos inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "El email ya está registrado"
                    }
                }
            }
        }
    }
)
async def register(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Registrar nuevo usuario"""
    auth_service = AuthService(db)
    ip_address = get_client_ip(request)
    
    return auth_service.register(user_data, ip_address)


@router.post(
    "/verify-token",
    response_model=ApiResponse,
    summary="Verificar token",
    description="Verificar si un token JWT es válido y no ha expirado."
)
async def verify_token(
    request: Request,
    token: str,
    db: Session = Depends(get_db)
):
    """Verificar validez de token"""
    auth_service = AuthService(db)
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    result = auth_service.verify_token(token, ip_address, user_agent)
    
    if result["valid"]:
        return ApiResponse(
            success=True,
            message="Token válido",
            data=result["payload"]
        )
    else:
        return ApiResponse(
            success=False,
            message="Token inválido"
        )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Renovar token",
    description="Renovar un token JWT válido por uno nuevo."
)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Renovar token de acceso"""
    auth_service = AuthService(db)    # Crear nuevo token para el usuario actual
    from app.core.security_utils import SecurityUtils
    from datetime import timedelta
    from app.core.config import settings
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = SecurityUtils.create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/logout",
    response_model=ApiResponse,
    summary="Cerrar sesión",
    description="Cerrar sesión del usuario actual."
)
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cerrar sesión"""
    auth_service = AuthService(db)
    ip_address = get_client_ip(request)
    
    auth_service.logout(current_user.id, ip_address)
    
    return ApiResponse(
        success=True,
        message="Sesión cerrada exitosamente"
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Información del usuario",
    description="Obtener información del usuario autenticado actual."
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Obtener información del usuario actual"""
    return UserResponse.model_validate(current_user)
