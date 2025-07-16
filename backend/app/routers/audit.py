from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_

from app.db.database import get_db
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.audit import AuditLogResponse, AuditLogStatsResponse
from app.services.audit import AuditService
from app.deps.auth import get_current_user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario actual es admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user

router = APIRouter()


@router.get("/logs", response_model=Dict[str, Any])
async def get_audit_logs(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    action: Optional[str] = Query(None, description="Filtrar por tipo de acción"),
    resource: Optional[str] = Query(None, description="Filtrar por recurso"),
    user_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    start_date: Optional[datetime] = Query(None, description="Fecha de inicio (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Fecha de fin (ISO format)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Obtener logs de auditoría con filtros avanzados
    Requiere permisos de administrador
    """
    audit_service = AuditService(db)
    
    # Construir query base
    query = db.query(AuditLog)
    
    # Aplicar filtros
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))
    
    if resource:
        query = query.filter(AuditLog.resource.ilike(f"%{resource}%"))
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    
    # Obtener total para paginación
    total = query.count()
    
    # Aplicar ordenamiento y paginación
    logs = query.order_by(desc(AuditLog.timestamp)).offset(skip).limit(limit).all()
    
    # Convertir a formato de respuesta
    log_responses = []
    for log in logs:
        # Obtener información del usuario si existe
        user_email = None
        if log.user_id:
            user = db.query(User).filter(User.id == log.user_id).first()
            if user:
                user_email = user.email
        
        log_response = AuditLogResponse(
            id=log.id,
            user_id=log.user_id,
            user_email=user_email,
            action=log.action,
            resource=log.resource,
            resource_id=log.resource_id,
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            details=log.details,
            timestamp=log.timestamp
        )
        log_responses.append(log_response)
    
    # Log de auditoría para esta consulta
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="READ",
        resource="audit_logs",
        details=f"Consulta de logs (skip: {skip}, limit: {limit}, filtros aplicados)"
    )
    
    return {
        "logs": log_responses,
        "total": total,
        "skip": skip,
        "limit": limit,
        "filters": {
            "action": action,
            "resource": resource,
            "user_id": user_id,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }
    }


@router.get("/stats", response_model=AuditLogStatsResponse)
async def get_audit_stats(
    days: int = Query(30, ge=1, le=365, description="Número de días para las estadísticas"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Obtener estadísticas de auditoría
    Requiere permisos de administrador
    """
    audit_service = AuditService(db)
    
    # Calcular fecha de inicio
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Query base para el período
    base_query = db.query(AuditLog).filter(AuditLog.timestamp >= start_date)
    
    # Total de acciones en el período
    total_actions = base_query.count()
    
    # Acciones por tipo
    actions_by_type = base_query.with_entities(
        AuditLog.action,
        func.count(AuditLog.id).label('count')
    ).group_by(AuditLog.action).all()
    
    actions_stats = {action: count for action, count in actions_by_type}
    
    # Acciones por recurso
    resources_by_type = base_query.with_entities(
        AuditLog.resource,
        func.count(AuditLog.id).label('count')
    ).group_by(AuditLog.resource).all()
    
    resources_stats = {resource: count for resource, count in resources_by_type}
    
    # Usuarios más activos
    active_users = base_query.filter(AuditLog.user_id.isnot(None)).with_entities(
        AuditLog.user_id,
        func.count(AuditLog.id).label('count')
    ).group_by(AuditLog.user_id).order_by(desc('count')).limit(10).all()
    
    # Obtener información de usuarios
    users_stats = []
    for user_id, count in active_users:
        user = db.query(User).filter(User.id == user_id).first()
        users_stats.append({
            "user_id": user_id,
            "user_email": user.email if user else f"Usuario {user_id}",
            "actions_count": count
        })
    
    # IPs más frecuentes
    frequent_ips = base_query.filter(AuditLog.ip_address.isnot(None)).with_entities(
        AuditLog.ip_address,
        func.count(AuditLog.id).label('count')
    ).group_by(AuditLog.ip_address).order_by(desc('count')).limit(10).all()
    
    ips_stats = [{"ip": ip, "count": count} for ip, count in frequent_ips]
    
    # Acciones por día (últimos 7 días para el gráfico)
    last_week = datetime.utcnow() - timedelta(days=7)
    daily_actions = base_query.filter(AuditLog.timestamp >= last_week).with_entities(
        func.date(AuditLog.timestamp).label('date'),
        func.count(AuditLog.id).label('count')
    ).group_by(func.date(AuditLog.timestamp)).order_by('date').all()
    
    daily_stats = [{"date": str(date), "count": count} for date, count in daily_actions]
    
    # Acciones por hora del día (promedio)
    hourly_actions = base_query.with_entities(
        func.extract('hour', AuditLog.timestamp).label('hour'),
        func.count(AuditLog.id).label('count')
    ).group_by(func.extract('hour', AuditLog.timestamp)).order_by('hour').all()
    
    hourly_stats = [{"hour": int(hour), "count": count} for hour, count in hourly_actions]
    
    # Log de auditoría para esta consulta
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="READ",
        resource="audit_stats",
        details=f"Consulta de estadísticas ({days} días)"
    )
    
    return AuditLogStatsResponse(
        period_days=days,
        start_date=start_date,
        end_date=datetime.utcnow(),
        total_actions=total_actions,
        actions_by_type=actions_stats,
        resources_by_type=resources_stats,
        most_active_users=users_stats,
        frequent_ips=ips_stats,
        daily_actions=daily_stats,
        hourly_distribution=hourly_stats
    )


@router.get("/actions", response_model=List[str])
async def get_available_actions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Obtener lista de tipos de acciones disponibles
    """
    actions = db.query(AuditLog.action).distinct().all()
    return [action[0] for action in actions if action[0]]


@router.get("/resources", response_model=List[str])
async def get_available_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Obtener lista de recursos disponibles
    """
    resources = db.query(AuditLog.resource).distinct().all()
    return [resource[0] for resource in resources if resource[0]]


@router.get("/export")
async def export_audit_logs(
    format: str = Query("csv", regex="^(csv|json)$", description="Formato de exportación"),
    start_date: Optional[datetime] = Query(None, description="Fecha de inicio"),
    end_date: Optional[datetime] = Query(None, description="Fecha de fin"),
    action: Optional[str] = Query(None, description="Filtrar por acción"),
    resource: Optional[str] = Query(None, description="Filtrar por recurso"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Exportar logs de auditoría en CSV o JSON
    """
    from fastapi.responses import StreamingResponse
    import csv
    import json
    from io import StringIO
    
    audit_service = AuditService(db)
    
    # Construir query
    query = db.query(AuditLog)
    
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))
    if resource:
        query = query.filter(AuditLog.resource.ilike(f"%{resource}%"))
    
    logs = query.order_by(desc(AuditLog.timestamp)).all()
    
    # Log de auditoría para exportación
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="EXPORT",
        resource="audit_logs",
        details=f"Exportación en formato {format} ({len(logs)} registros)"
    )
    
    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            "ID", "User ID", "Action", "Resource", "Resource ID",
            "IP Address", "User Agent", "Details", "Timestamp"
        ])
        
        # Data
        for log in logs:
            writer.writerow([
                log.id, log.user_id, log.action, log.resource, log.resource_id,
                log.ip_address, log.user_agent, log.details, log.timestamp
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
    
    else:  # JSON
        data = []
        for log in logs:
            data.append({
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource": log.resource,
                "resource_id": log.resource_id,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "details": log.details,
                "timestamp": log.timestamp.isoformat() if log.timestamp else None
            })
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        return StreamingResponse(
            iter([json_str]),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"}
        )


@router.delete("/logs/{log_id}")
async def delete_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Eliminar un log de auditoría específico
    ADVERTENCIA: Esta acción debe usarse con extrema precaución
    """
    audit_service = AuditService(db)
    
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log de auditoría no encontrado"
        )
    
    # Log de auditoría antes de eliminar
    audit_service.create_audit_log(
        user_id=current_user.id,
        action="DELETE",
        resource="audit_logs",
        resource_id=log_id,
        details=f"Eliminación de log: {log.action} en {log.resource}"
    )
    
    db.delete(log)
    db.commit()
    
    return {"message": "Log de auditoría eliminado exitosamente"}


@router.post("/cleanup")
async def cleanup_old_logs(
    days_to_keep: int = Query(90, ge=30, le=3650, description="Días de logs a mantener"),
    dry_run: bool = Query(True, description="Simulación sin eliminar datos"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Limpiar logs de auditoría antiguos
    Por defecto es una simulación (dry_run=True)
    """
    audit_service = AuditService(db)
    
    cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
    
    # Contar logs que serían eliminados
    old_logs_count = db.query(AuditLog).filter(AuditLog.timestamp < cutoff_date).count()
    
    if dry_run:
        # Solo simulación
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="SIMULATE_CLEANUP",
            resource="audit_logs",
            details=f"Simulación de limpieza: {old_logs_count} logs serían eliminados (>{days_to_keep} días)"
        )
        
        return {
            "message": "Simulación de limpieza completada",
            "logs_to_delete": old_logs_count,
            "cutoff_date": cutoff_date.isoformat(),
            "dry_run": True
        }
    else:
        # Eliminación real
        deleted_count = db.query(AuditLog).filter(AuditLog.timestamp < cutoff_date).delete()
        db.commit()
        
        audit_service.create_audit_log(
            user_id=current_user.id,
            action="CLEANUP",
            resource="audit_logs",
            details=f"Limpieza realizada: {deleted_count} logs eliminados (>{days_to_keep} días)"
        )
        
        return {
            "message": "Limpieza de logs completada",
            "logs_deleted": deleted_count,
            "cutoff_date": cutoff_date.isoformat(),
            "dry_run": False
        }
