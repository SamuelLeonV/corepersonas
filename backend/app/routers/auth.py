from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import Token, LoginRequest, UserCreate, UserResponse
from app.models.user import User
from app.schemas.common import ApiResponse
from app.services.user import UserService
from app.services.auth import AuthService
from app.core.security_service import SecurityService
from app.core.security_utils import SecurityUtils
from app.services.audit import AuditService
from app.deps.auth import get_current_user
from app.core.config import settings


def get_client_ip(request: Request) -> str:
    """Obtener la IP del cliente"""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """Obtener el User-Agent del cliente"""
    return request.headers.get("User-Agent", "unknown")

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
        },
        423: {
            "description": "Cuenta bloqueada por múltiples intentos fallidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Cuenta bloqueada temporalmente por múltiples intentos fallidos"
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
    """
    Iniciar sesión en el sistema.
    
    - **email**: Email del usuario registrado
    - **password**: Contraseña del usuario
    
    **Características de seguridad:**
    - Bloqueo automático tras 5 intentos fallidos
    - Logging de auditoría de todos los intentos
    - Token JWT con expiración de 30 minutos
    - Registro de IP y User-Agent
    """
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    auth_service = AuthService(db)
    audit_service = AuditService(db)
    
    # Autenticar usuario
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        # Log de intento fallido
        audit_service.create_audit_log(
            user_id=None,
            action="LOGIN_FAILED",
            resource="auth",
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Intento de login fallido para email: {login_data.email}"
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = SecurityUtils.create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    # Log de login exitoso
    audit_service.create_audit_log(
        user_id=user.id,
        action="LOGIN_SUCCESS",
        resource="auth",
        ip_address=client_ip,
        user_agent=user_agent,
        details=f"Login exitoso para usuario: {user.email}"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register", 
    response_model=ApiResponse,
    summary="Registrar nuevo usuario",
    description="Crear una nueva cuenta de usuario en el sistema",
    responses={
        201: {
            "description": "Usuario creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Usuario creado exitosamente",
                        "data": {
                            "id": 1,
                            "email": "usuario@ejemplo.com",
                            "is_active": True,
                            "is_admin": False
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
                        "detail": "El email ya está registrado"
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
                                "loc": ["body", "password"],
                                "msg": "ensure this value has at least 8 characters",
                                "type": "value_error.any_str.min_length"
                            }
                        ]
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
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    try:
        # Crear usuario (autoregistro, sin created_by)
        user = user_service.create_user_direct(user_data)
        
        # Log de registro exitoso
        audit_service.create_audit_log(
            user_id=user.id,
            action="REGISTER_SUCCESS",
            resource="auth",
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Usuario registrado: {user.email}"
        )
        
        return ApiResponse(
            success=True,
            message="Usuario registrado exitosamente",
            data={"user_id": user.id, "email": user.email}
        )
        
    except HTTPException as e:
        # Log de registro fallido
        audit_service.create_audit_log(
            user_id=None,
            action="REGISTER_FAILED",
            resource="auth",
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Registro fallido para email: {user_data.email} - {str(e.detail)}"
        )
        raise e


@router.post("/verify-token", response_model=ApiResponse)
async def verify_token(current_user: User = Depends(get_current_user)):
    """Verificar token de acceso"""
    return ApiResponse(
        success=True,
        message="Token válido",
        data={
            "user_id": current_user.id,
            "email": current_user.email,
            "is_admin": current_user.is_admin,
            "is_active": current_user.is_active
        }
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Renovar token de acceso"""
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    audit_service = AuditService(db)
    
    # Crear nuevo token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = SecurityUtils.create_access_token(
        data={"sub": current_user.email}, 
        expires_delta=access_token_expires
    )
    
    # Log de renovación
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="TOKEN_REFRESH",
        resource="auth",
        ip_address=client_ip,
        user_agent=user_agent,
        details=f"Token renovado para usuario: {current_user.email}"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", response_model=ApiResponse)
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cerrar sesión"""
    
    # Obtener información del cliente
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Servicios
    audit_service = AuditService(db)
    
    # Log de logout
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="LOGOUT",
        resource="auth",
        ip_address=client_ip,
        user_agent=user_agent,
        details=f"Logout para usuario: {current_user.email}"
    )
    
    return ApiResponse(
        success=True,
        message="Sesión cerrada exitosamente"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return current_user
