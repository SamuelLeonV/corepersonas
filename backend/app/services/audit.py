"""
Servicio para operaciones de auditoría.
"""

from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
from app.schemas.audit import AuditLogResponse, AuditLogStatsResponse
from app.repositories.audit import AuditRepository
from app.repositories.user import UserRepository


class AuditService:
    """Servicio para operaciones de auditoría"""
    
    def __init__(self, db: Session):
        self.db = db
        self.audit_repo = AuditRepository(db)
        self.user_repo = UserRepository(db)
    
    def get_audit_logs(self, skip: int = 0, limit: int = 100, user_id: int = None, ip_address: str = None) -> List[AuditLogResponse]:
        """Obtener logs de auditoría"""
        logs = self.audit_repo.get_logs(skip=skip, limit=limit)
        
        # Enriquecer con información del usuario
        result = []
        for log in logs:
            log_response = AuditLogResponse.model_validate(log)
            
            # Agregar email del usuario si existe
            if log.user_id:
                user = self.user_repo.get(log.user_id)
                if user:
                    log_response.user_email = user.email
            
            result.append(log_response)
        
        # Log de consulta de auditoría
        self.audit_repo.create_log(
            user_id=user_id,
            action="READ",
            resource="audit_logs",
            ip_address=ip_address,
            details=f"Consulta de logs de auditoría: {len(logs)} registros"
        )
        
        return result
    
    def get_audit_logs_by_user(self, target_user_id: int, skip: int = 0, limit: int = 100, 
                              user_id: int = None, ip_address: str = None) -> List[AuditLogResponse]:
        """Obtener logs de auditoría por usuario"""
        logs = self.audit_repo.get_logs_by_user(target_user_id, skip=skip, limit=limit)
        
        # Enriquecer con información del usuario
        result = []
        for log in logs:
            log_response = AuditLogResponse.model_validate(log)
            
            # Agregar email del usuario si existe
            if log.user_id:
                user = self.user_repo.get(log.user_id)
                if user:
                    log_response.user_email = user.email
            
            result.append(log_response)
        
        # Log de consulta de auditoría
        self.audit_repo.create_log(
            user_id=user_id,
            action="READ",
            resource="audit_logs",
            ip_address=ip_address,
            details=f"Consulta de logs por usuario {target_user_id}: {len(logs)} registros"
        )
        
        return result
    
    def get_audit_logs_by_action(self, action: str, skip: int = 0, limit: int = 100, 
                                user_id: int = None, ip_address: str = None) -> List[AuditLogResponse]:
        """Obtener logs de auditoría por acción"""
        logs = self.audit_repo.get_logs_by_action(action, skip=skip, limit=limit)
        
        # Enriquecer con información del usuario
        result = []
        for log in logs:
            log_response = AuditLogResponse.model_validate(log)
            
            # Agregar email del usuario si existe
            if log.user_id:
                user = self.user_repo.get(log.user_id)
                if user:
                    log_response.user_email = user.email
            
            result.append(log_response)
        
        # Log de consulta de auditoría
        self.audit_repo.create_log(
            user_id=user_id,
            action="READ",
            resource="audit_logs",
            ip_address=ip_address,
            details=f"Consulta de logs por acción {action}: {len(logs)} registros"
        )
        
        return result
    
    def get_audit_logs_by_resource(self, resource: str, resource_id: int = None, 
                                  skip: int = 0, limit: int = 100, 
                                  user_id: int = None, ip_address: str = None) -> List[AuditLogResponse]:
        """Obtener logs de auditoría por recurso"""
        logs = self.audit_repo.get_logs_by_resource(resource, resource_id, skip=skip, limit=limit)
        
        # Enriquecer con información del usuario
        result = []
        for log in logs:
            log_response = AuditLogResponse.model_validate(log)
            
            # Agregar email del usuario si existe
            if log.user_id:
                user = self.user_repo.get(log.user_id)
                if user:
                    log_response.user_email = user.email
            
            result.append(log_response)
        
        # Log de consulta de auditoría
        resource_filter = f"{resource}:{resource_id}" if resource_id else resource
        self.audit_repo.create_log(
            user_id=user_id,
            action="READ",
            resource="audit_logs",
            ip_address=ip_address,
            details=f"Consulta de logs por recurso {resource_filter}: {len(logs)} registros"
        )
        
        return result
    
    def get_audit_logs_by_period(self, start_date: datetime, end_date: datetime, 
                                skip: int = 0, limit: int = 100, 
                                user_id: int = None, ip_address: str = None) -> List[AuditLogResponse]:
        """Obtener logs de auditoría por período"""
        logs = self.audit_repo.get_logs_by_period(start_date, end_date, skip=skip, limit=limit)
        
        # Enriquecer con información del usuario
        result = []
        for log in logs:
            log_response = AuditLogResponse.model_validate(log)
            
            # Agregar email del usuario si existe
            if log.user_id:
                user = self.user_repo.get(log.user_id)
                if user:
                    log_response.user_email = user.email
            
            result.append(log_response)
        
        # Log de consulta de auditoría
        self.audit_repo.create_log(
            user_id=user_id,
            action="READ",
            resource="audit_logs",
            ip_address=ip_address,
            details=f"Consulta de logs por período {start_date} - {end_date}: {len(logs)} registros"
        )
        
        return result
    
    def get_audit_stats(self, days: int = 30, user_id: int = None, ip_address: str = None) -> AuditLogStatsResponse:
        """Obtener estadísticas de auditoría"""
        stats = self.audit_repo.get_stats(days)
        
        # Enriquecer usuarios más activos con emails
        most_active_users = []
        for user_stats in stats['most_active_users']:
            user = self.user_repo.get(user_stats['user_id'])
            user_info = {
                'user_id': user_stats['user_id'],
                'actions_count': user_stats['actions_count'],
                'user_email': user.email if user else 'Usuario eliminado'
            }
            most_active_users.append(user_info)
        
        stats['most_active_users'] = most_active_users
        
        # Log de consulta de estadísticas
        self.audit_repo.create_log(
            user_id=user_id,
            action="STATS",
            resource="audit_stats",
            ip_address=ip_address,
            details=f"Consulta de estadísticas de auditoría: {days} días"
        )
        
        return AuditLogStatsResponse(**stats)
    
    def create_audit_log(self, user_id: int, action: str, resource: str, 
                        resource_id: int = None, ip_address: str = None,
                        user_agent: str = None, details: str = None) -> AuditLogResponse:
        """Crear log de auditoría"""
        log = self.audit_repo.create_log(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        
        # Enriquecer con información del usuario
        log_response = AuditLogResponse.model_validate(log)
        if log.user_id:
            user = self.user_repo.get(log.user_id)
            if user:
                log_response.user_email = user.email
        
        return log_response
    
    def export_audit_logs(self, format: str = "csv", user_id: int = None,
                       action: str = None, resource: str = None,
                       resource_id: int = None, start_date: datetime = None,
                       end_date: datetime = None, ip_address: str = None) -> List[AuditLogResponse]:
        """Exportar logs de auditoría en formato CSV o JSON"""
        # Preparar fechas
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
            
        # Configurar filtros
        filters = {}
        if user_id is not None:
            filters["user_id"] = user_id
        if action is not None:
            filters["action"] = action
        if resource is not None:
            filters["resource"] = resource
        if resource_id is not None:
            filters["resource_id"] = resource_id
            
        # Obtener logs
        logs = self.audit_repo.get_logs_filtered(
            start_date=start_date,
            end_date=end_date,
            skip=0,
            limit=10000,
            **filters
        )
        
        # Registrar acción de exportación
        self.audit_repo.create_log(
            user_id=user_id,
            action="EXPORT",
            resource="audit_logs",
            ip_address=ip_address,
            details=f"Exportación de {len(logs)} logs en formato {format}"
        )
        
        # Enriquecer con información del usuario
        result = []
        for log in logs:
            log_response = AuditLogResponse.model_validate(log)
            
            # Agregar email del usuario si existe
            if log.user_id:
                user = self.user_repo.get(log.user_id)
                if user:
                    log_response.user_email = user.email
            
            result.append(log_response)
        
        return result
