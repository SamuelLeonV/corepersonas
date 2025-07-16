"""
Repositorio para operaciones de auditoría.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from app.models.audit_log import AuditLog
from app.repositories.base import BaseRepository


class AuditRepository:
    """Repositorio para operaciones de auditoría"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_log(self, user_id: Optional[int], action: str, resource: str, 
                   resource_id: Optional[int] = None, ip_address: Optional[str] = None,
                   user_agent: Optional[str] = None, details: Optional[str] = None) -> AuditLog:
        """Crear log de auditoría"""
        db_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log
    
    def get_logs(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Obtener logs de auditoría"""
        return self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    def get_logs_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Obtener logs de auditoría por usuario"""
        return self.db.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    def get_logs_by_action(self, action: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Obtener logs de auditoría por acción"""
        return self.db.query(AuditLog).filter(
            AuditLog.action == action
        ).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    def get_logs_by_resource(self, resource: str, resource_id: Optional[int] = None,
                           skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Obtener logs de auditoría por recurso"""
        query = self.db.query(AuditLog).filter(AuditLog.resource == resource)
        
        if resource_id:
            query = query.filter(AuditLog.resource_id == resource_id)
        
        return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    def get_logs_by_period(self, start_date: datetime, end_date: datetime,
                          skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Obtener logs de auditoría por período"""
        return self.db.query(AuditLog).filter(
            and_(AuditLog.timestamp >= start_date, AuditLog.timestamp <= end_date)
        ).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    def get_stats(self, days: int = 30) -> Dict:
        """Obtener estadísticas de auditoría"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Total de acciones
        total_actions = self.db.query(AuditLog).filter(
            AuditLog.timestamp >= start_date
        ).count()
        
        # Acciones por tipo
        actions_by_type = dict(
            self.db.query(AuditLog.action, func.count(AuditLog.id))
            .filter(AuditLog.timestamp >= start_date)
            .group_by(AuditLog.action)
            .all()
        )
        
        # Recursos por tipo
        resources_by_type = dict(
            self.db.query(AuditLog.resource, func.count(AuditLog.id))
            .filter(AuditLog.timestamp >= start_date)
            .group_by(AuditLog.resource)
            .all()
        )
        
        # Usuarios más activos
        most_active_users = self.db.query(
            AuditLog.user_id,
            func.count(AuditLog.id).label('actions_count')
        ).filter(
            and_(AuditLog.timestamp >= start_date, AuditLog.user_id.isnot(None))
        ).group_by(AuditLog.user_id).order_by(
            func.count(AuditLog.id).desc()
        ).limit(10).all()
        
        # IPs más frecuentes
        frequent_ips = self.db.query(
            AuditLog.ip_address,
            func.count(AuditLog.id).label('count')
        ).filter(
            and_(AuditLog.timestamp >= start_date, AuditLog.ip_address.isnot(None))
        ).group_by(AuditLog.ip_address).order_by(
            func.count(AuditLog.id).desc()
        ).limit(10).all()
        
        # Acciones por día
        daily_actions = self.db.query(
            func.date(AuditLog.timestamp).label('date'),
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.timestamp >= start_date
        ).group_by(
            func.date(AuditLog.timestamp)
        ).order_by(
            func.date(AuditLog.timestamp)
        ).all()
        
        # Distribución por hora
        hourly_distribution = self.db.query(
            func.extract('hour', AuditLog.timestamp).label('hour'),
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.timestamp >= start_date
        ).group_by(
            func.extract('hour', AuditLog.timestamp)
        ).order_by(
            func.extract('hour', AuditLog.timestamp)
        ).all()
        
        return {
            'period_days': days,
            'start_date': start_date,
            'end_date': end_date,
            'total_actions': total_actions,
            'actions_by_type': actions_by_type,
            'resources_by_type': resources_by_type,
            'most_active_users': [{'user_id': user_id, 'actions_count': count} for user_id, count in most_active_users],
            'frequent_ips': [{'ip': ip, 'count': count} for ip, count in frequent_ips],
            'daily_actions': [{'date': str(date), 'count': count} for date, count in daily_actions],
            'hourly_distribution': [{'hour': int(hour), 'count': count} for hour, count in hourly_distribution]
        }
    
    def count(self) -> int:
        """Contar total de logs"""
        return self.db.query(AuditLog).count()
    
    def count_by_user(self, user_id: int) -> int:
        """Contar logs por usuario"""
        return self.db.query(AuditLog).filter(AuditLog.user_id == user_id).count()
    
    def count_by_action(self, action: str) -> int:
        """Contar logs por acción"""
        return self.db.query(AuditLog).filter(AuditLog.action == action).count()
    
    def get_logs_filtered(self, start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None,
                        user_id: Optional[int] = None,
                        action: Optional[str] = None,
                        resource: Optional[str] = None,
                        resource_id: Optional[int] = None,
                        skip: int = 0, 
                        limit: int = 100) -> List[AuditLog]:
        """Obtener logs de auditoría con múltiples filtros"""
        query = self.db.query(AuditLog)
        
        # Aplicar filtros si están presentes
        if start_date and end_date:
            query = query.filter(and_(AuditLog.timestamp >= start_date, AuditLog.timestamp <= end_date))
        
        if user_id is not None:
            query = query.filter(AuditLog.user_id == user_id)
        
        if action:
            query = query.filter(AuditLog.action == action)
        
        if resource:
            query = query.filter(AuditLog.resource == resource)
        
        if resource_id is not None:
            query = query.filter(AuditLog.resource_id == resource_id)
        
        return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
