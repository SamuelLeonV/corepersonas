"""
Esquemas Pydantic para auditoría.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AuditLogResponse(BaseModel):
    """Esquema de respuesta para logs de auditoría"""
    id: int
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    action: str
    resource: str
    resource_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[str] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "user_email": "admin@auditoria.com",
                "action": "CREATE",
                "resource": "persons",
                "resource_id": 5,
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0...",
                "details": "Persona creada: Juan Pérez",
                "timestamp": "2025-07-13T10:30:00Z"
            }
        }


class AuditLogStatsResponse(BaseModel):
    """Esquema de respuesta para estadísticas de auditoría"""
    period_days: int
    start_date: datetime
    end_date: datetime
    total_actions: int
    actions_by_type: dict
    resources_by_type: dict
    most_active_users: List[dict]
    frequent_ips: List[dict]
    daily_actions: List[dict]
    hourly_distribution: List[dict]
    
    class Config:
        json_schema_extra = {
            "example": {
                "period_days": 30,
                "start_date": "2025-06-13T10:30:00Z",
                "end_date": "2025-07-13T10:30:00Z",
                "total_actions": 1250,
                "actions_by_type": {
                    "CREATE": 300,
                    "READ": 800,
                    "UPDATE": 120,
                    "DELETE": 30
                },
                "resources_by_type": {
                    "persons": 950,
                    "users": 200,
                    "audit_logs": 100
                },
                "most_active_users": [
                    {"user_id": 1, "user_email": "admin@auditoria.com", "actions_count": 450},
                    {"user_id": 2, "user_email": "usuario@ejemplo.com", "actions_count": 250}
                ],
                "frequent_ips": [
                    {"ip": "192.168.1.100", "count": 600},
                    {"ip": "10.0.0.50", "count": 400}
                ],
                "daily_actions": [
                    {"date": "2025-07-06", "count": 85},
                    {"date": "2025-07-07", "count": 92}
                ],
                "hourly_distribution": [
                    {"hour": 9, "count": 125},
                    {"hour": 10, "count": 145}
                ]
            }
        }
