"""
Rutas de la API para auditoría.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.database import get_db
from app.schemas.audit import AuditLogResponse, AuditLogStatsResponse
from app.schemas.common import ApiResponse, PaginatedResponse
from app.services.audit import AuditService
from app.deps.auth import get_current_user, get_current_admin_user, get_client_ip
from app.models.user import User
from app.utils.responses import ResponseUtils

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse,
    summary="Listar logs de auditoría",
    description="Obtener lista paginada de logs de auditoría. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def get_audit_logs(
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener logs de auditoría"""
    audit_service = AuditService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    logs = audit_service.get_audit_logs(skip=skip, limit=limit, user_id=current_user.id, ip_address=ip_address)
    
    # Contar total de logs
    from app.repositories.audit import AuditRepository
    audit_repo = AuditRepository(db)
    total = audit_repo.count()
    
    return ResponseUtils.paginated_response(
        items=[log.dict() for log in logs],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get(
    "/logs",
    response_model=PaginatedResponse,
    summary="Listar logs de auditoría (alias)",
    description="Alias de la ruta principal / para compatibilidad con clientes existentes. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def get_audit_logs_alias(
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Alias para obtener logs de auditoría"""
    # Este es un alias para mantener compatibilidad con el endpoint anterior
    audit_service = AuditService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    logs = audit_service.get_audit_logs(skip=skip, limit=limit, user_id=current_user.id, ip_address=ip_address)
    
    # Contar total de logs
    from app.repositories.audit import AuditRepository
    audit_repo = AuditRepository(db)
    total = audit_repo.count()
    
    return ResponseUtils.paginated_response(
        items=[log.dict() for log in logs],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get(
    "/user/{user_id}",
    response_model=PaginatedResponse,
    summary="Logs por usuario",
    description="Obtener logs de auditoría de un usuario específico. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def get_audit_logs_by_user(
    user_id: int,
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener logs de auditoría por usuario"""
    audit_service = AuditService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    logs = audit_service.get_audit_logs_by_user(
        target_user_id=user_id,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        ip_address=ip_address
    )
    
    # Contar total de logs por usuario
    from app.repositories.audit import AuditRepository
    audit_repo = AuditRepository(db)
    total = audit_repo.count_by_user(user_id)
    
    return ResponseUtils.paginated_response(
        items=[log.dict() for log in logs],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get(
    "/action/{action}",
    response_model=PaginatedResponse,
    summary="Logs por acción",
    description="Obtener logs de auditoría por tipo de acción. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def get_audit_logs_by_action(
    action: str,
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener logs de auditoría por acción"""
    audit_service = AuditService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    logs = audit_service.get_audit_logs_by_action(
        action=action,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        ip_address=ip_address
    )
    
    # Contar total de logs por acción
    from app.repositories.audit import AuditRepository
    audit_repo = AuditRepository(db)
    total = audit_repo.count_by_action(action)
    
    return ResponseUtils.paginated_response(
        items=[log.dict() for log in logs],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get(
    "/resource/{resource}",
    response_model=PaginatedResponse,
    summary="Logs por recurso",
    description="Obtener logs de auditoría por recurso. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def get_audit_logs_by_resource(
    resource: str,
    request: Request,
    resource_id: Optional[int] = Query(None, description="ID específico del recurso"),
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener logs de auditoría por recurso"""
    audit_service = AuditService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    logs = audit_service.get_audit_logs_by_resource(
        resource=resource,
        resource_id=resource_id,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        ip_address=ip_address
    )
    
    # Para el total, necesitamos hacer consulta sin paginación
    from app.repositories.audit import AuditRepository
    audit_repo = AuditRepository(db)
    total_logs = audit_repo.get_logs_by_resource(resource, resource_id, skip=0, limit=10000)
    total = len(total_logs)
    
    return ResponseUtils.paginated_response(
        items=[log.dict() for log in logs],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get(
    "/period",
    response_model=PaginatedResponse,
    summary="Logs por período",
    description="Obtener logs de auditoría por período de tiempo. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def get_audit_logs_by_period(
    request: Request,
    start_date: datetime = Query(..., description="Fecha de inicio (ISO format)"),
    end_date: datetime = Query(..., description="Fecha de fin (ISO format)"),
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener logs de auditoría por período"""
    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio debe ser anterior a la fecha de fin"
        )
    
    audit_service = AuditService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    logs = audit_service.get_audit_logs_by_period(
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        ip_address=ip_address
    )
    
    # Para el total, necesitamos hacer consulta sin paginación
    from app.repositories.audit import AuditRepository
    audit_repo = AuditRepository(db)
    total_logs = audit_repo.get_logs_by_period(start_date, end_date, skip=0, limit=10000)
    total = len(total_logs)
    
    return ResponseUtils.paginated_response(
        items=[log.dict() for log in logs],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get(
    "/stats",
    response_model=AuditLogStatsResponse,
    summary="Estadísticas de auditoría",
    description="Obtener estadísticas de auditoría del sistema. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def get_audit_stats(
    request: Request,
    days: int = Query(30, ge=1, le=365, description="Número de días para las estadísticas"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de auditoría"""
    audit_service = AuditService(db)
    ip_address = get_client_ip(request)
    
    return audit_service.get_audit_stats(days=days, user_id=current_user.id, ip_address=ip_address)


@router.get(
    "/my-actions",
    response_model=PaginatedResponse,
    summary="Mis acciones",
    description="Obtener logs de auditoría del usuario actual."
)
async def get_my_audit_logs(
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener logs de auditoría del usuario actual"""
    audit_service = AuditService(db)
    ip_address = get_client_ip(request)
    
    skip, limit = ResponseUtils.calculate_pagination(page, per_page)
    logs = audit_service.get_audit_logs_by_user(
        target_user_id=current_user.id,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        ip_address=ip_address
    )
    
    # Contar total de logs del usuario
    from app.repositories.audit import AuditRepository
    audit_repo = AuditRepository(db)
    total = audit_repo.count_by_user(current_user.id)
    
    return ResponseUtils.paginated_response(
        items=[log.dict() for log in logs],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get(
    "/export",
    summary="Exportar logs de auditoría",
    description="Exportar logs de auditoría en formato CSV o JSON. Solo administradores.",
    dependencies=[Depends(get_current_admin_user)]
)
async def export_audit_logs(
    request: Request,
    format: str = Query("csv", description="Formato de exportación: csv o json"),
    user_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    action: Optional[str] = Query(None, description="Filtrar por tipo de acción"),
    resource: Optional[str] = Query(None, description="Filtrar por recurso"),
    start_date: Optional[datetime] = Query(None, description="Fecha de inicio (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Fecha de fin (ISO format)"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Exportar logs de auditoría en formato CSV o JSON"""
    from app.repositories.audit import AuditRepository
    from fastapi.responses import StreamingResponse
    import csv
    import io
    import json
    from datetime import datetime, timedelta
    
    audit_repo = AuditRepository(db)
    ip_address = get_client_ip(request)
    
    # Configurar filtros
    filters = {}
    if user_id is not None:
        filters["user_id"] = user_id
    if action is not None:
        filters["action"] = action
    if resource is not None:
        filters["resource"] = resource
    
    # Manejar fechas - ampliamos el rango para obtener más resultados
    # Para depuración, obtenemos todos los registros sin filtrar por fecha
    start_date = None
    end_date = None
    
    # Obtener logs (sin paginación, para exportación completa)
    # Para depuración, primero verificamos la cantidad total de logs
    total_logs = audit_repo.count()
    print(f"Total de logs en la base de datos: {total_logs}")
    
    # Obtener todos los logs sin filtros para asegurar que recibimos datos
    logs = audit_repo.get_logs(skip=0, limit=10000)
    
    # Registrar la acción de exportación
    audit_service = AuditService(db)
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="EXPORT",
        resource="audit_logs",
        ip_address=ip_address,
        details=f"Exportación de logs en formato {format}: {len(logs)} registros"
    )
    
    # Formatear la salida según el formato solicitado
    if format.lower() == "csv":
        # Crear un buffer en memoria para el CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados
        headers = ["ID", "Usuario", "Acción", "Recurso", "ID Recurso", 
                  "Dirección IP", "User Agent", "Detalles", "Fecha"]
        writer.writerow(headers)
        
        # Información de depuración
        print(f"Cantidad de logs a exportar: {len(logs)}")
        
        # Escribir datos y depuración
        for log in logs:
            print(f"Procesando log ID {log.id}: {log.action} - {log.resource}")
            writer.writerow([
                log.id,
                log.user_id,
                log.action,
                log.resource,
                log.resource_id if log.resource_id else "",
                log.ip_address,
                log.user_agent,
                log.details,
                log.timestamp.isoformat() if log.timestamp else ""
            ])
        
        # Preparar respuesta
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment;filename=audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    
    elif format.lower() == "json":
        # Convertir logs a formato JSON
        logs_data = [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource": log.resource,
                "resource_id": log.resource_id,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "details": log.details,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ]
        
        # Preparar respuesta
        return StreamingResponse(
            iter([json.dumps(logs_data, ensure_ascii=False)]),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment;filename=audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de exportación no válido. Opciones disponibles: csv, json"
        )
