#!/usr/bin/env python3
"""
Utilidad para verificar el estado del sistema de auditoría
"""

import requests
import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.models import User, Person, AuditLog
from app.core.security_utils import SecurityUtils
from app.db.database import engine


def get_system_status():
    """Obtener estado completo del sistema"""
    status = {
        "timestamp": datetime.now().isoformat(),
        "api": None,
        "database": None,
        "statistics": None,
        "endpoints": get_api_endpoints(),  # Añadir endpoints al status
        "errors": []  # Añadir lista de errores detectados
    }
    
    # Verificar API
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            status["api"] = "OPERATIVA"
        else:
            status["api"] = f"ERROR - Status: {response.status_code}"
            status["errors"].append({
                "tipo": "API_ERROR",
                "mensaje": f"La API no está respondiendo correctamente. Status code: {response.status_code}",
                "solucion": "Revisar los logs del servidor y verificar que FastAPI esté ejecutándose sin errores."
            })
    except Exception as e:
        status["api"] = f"ERROR - {str(e)}"
        status["errors"].append({
            "tipo": "API_CONNECTION_ERROR",
            "mensaje": f"No se puede conectar con la API: {str(e)}",
            "solucion": "Verificar que el servidor FastAPI esté en ejecución en localhost:8000."
        })
    
    # Verificar base de datos
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Contar registros
        users_count = db.query(User).count()
        persons_count = db.query(Person).count()
        audit_logs_count = db.query(AuditLog).count()
        
        status["database"] = "OPERATIVA"
        status["statistics"] = {
            "users": users_count,
            "persons": persons_count,
            "audit_logs": audit_logs_count
        }
        
        # Comprobar problemas comunes en los registros
        if persons_count > 0:
            check_persons_data_issues(db, status)
        
        db.close()
        
    except Exception as e:
        status["database"] = f"ERROR - {str(e)}"
        status["statistics"] = None
        status["errors"].append({
            "tipo": "DATABASE_ERROR",
            "mensaje": f"Error al conectar con la base de datos: {str(e)}",
            "solucion": "Verificar que PostgreSQL esté en ejecución y las credenciales sean correctas."
        })
    
    # Verificar endpoints específicos para detectar errores
    if status["api"] == "OPERATIVA":
        check_critical_endpoints(status)
    
    return status


def check_persons_data_issues(db, status):
    """Verificar problemas comunes en los datos de personas"""
    try:
        # Comprobar RUT con formato incorrecto o muy largo
        large_ruts = db.query(Person).filter(Person.rut.like('%=%')).count()
        if large_ruts > 0:
            status["errors"].append({
                "tipo": "DATA_FORMAT_ERROR",
                "mensaje": f"Se encontraron {large_ruts} registros con RUTs en formato base64 o encriptado demasiado largo",
                "solucion": "Revisar la conversión de RUTs en app/schemas/person.py y asegurar que el campo rut en PersonResponse tiene max_length suficiente."
            })
            
        # Verificar campos requeridos faltantes
        missing_fields = db.query(Person).filter(
            (Person.religion_hash == None) | 
            (Person.religion_salt == None)
        ).count()
        
        if missing_fields > 0:
            status["errors"].append({
                "tipo": "MISSING_FIELDS",
                "mensaje": f"Se encontraron {missing_fields} registros con campos obligatorios faltantes (religion_hash o religion_salt)",
                "solucion": "Revisar el esquema PersonResponse y asegurar que maneja correctamente los campos nulos."
            })
    except Exception as e:
        status["errors"].append({
            "tipo": "DATA_CHECK_ERROR",
            "mensaje": f"Error al verificar datos de personas: {str(e)}",
            "solucion": "Revisar la estructura de la tabla persons y las consultas de validación."
        })


def check_critical_endpoints(status):
    """Verificar endpoints críticos para detectar errores comunes"""
    # Lista de endpoints críticos para comprobar
    critical_endpoints = [
        {"url": "http://localhost:8000/api/persons/?page=1&per_page=1", "name": "Listado de personas"},
        {"url": "http://localhost:8000/api/audit/?page=1&per_page=1", "name": "Logs de auditoría"}
    ]
    
    headers = {}
    # Intentar obtener un token de acceso para las solicitudes autenticadas
    try:
        auth_response = requests.post(
            "http://localhost:8000/api/auth/login", 
            json={"email": "admin@example.com", "password": "Admin123!"}, 
            timeout=5
        )
        if auth_response.status_code == 200:
            token = auth_response.json().get("access_token")
            if token:
                headers["Authorization"] = f"Bearer {token}"
    except Exception:
        # Si falla la autenticación, continuamos sin token
        pass
    
    # Verificar cada endpoint crítico
    for endpoint in critical_endpoints:
        try:
            response = requests.get(endpoint["url"], headers=headers, timeout=5)
            if response.status_code != 200:
                error_info = None
                try:
                    error_info = response.json()
                except:
                    error_info = {"detail": "No se pudo decodificar la respuesta"}
                
                status["errors"].append({
                    "tipo": "ENDPOINT_ERROR",
                    "endpoint": endpoint["name"],
                    "mensaje": f"Error en endpoint {endpoint['url']}: Status {response.status_code}",
                    "detalles": str(error_info),
                    "solucion": "Revisar los logs del servidor y la implementación del endpoint."
                })
        except Exception as e:
            status["errors"].append({
                "tipo": "ENDPOINT_CONNECTION_ERROR",
                "endpoint": endpoint["name"],
                "mensaje": f"No se pudo conectar con el endpoint {endpoint['url']}: {str(e)}",
                "solucion": "Verificar que el servidor esté respondiendo correctamente."
            })


def get_api_endpoints():
    """Obtener listado de endpoints de la API implementados en el backend"""
    return {
        "auth": {
            "login": "POST /api/auth/login",
            "register": "POST /api/auth/register", 
            "me": "GET /api/auth/me",
            "verify-token": "POST /api/auth/verify-token",
            "refresh": "POST /api/auth/refresh",
            "logout": "POST /api/auth/logout"
        },
        "users": {
            "list": "GET /api/users/",
            "create": "POST /api/users/",
            "get": "GET /api/users/{id}",
            "update": "PUT /api/users/{id}",
            "delete": "DELETE /api/users/{id}"
        },
        "persons": {
            "list": "GET /api/persons/",
            "create": "POST /api/persons/",
            "get": "GET /api/persons/{id}",
            "update": "PUT /api/persons/{id}",
            "delete": "DELETE /api/persons/{id}",
            "search_rut": "GET /api/persons/search/rut",
            "search_name": "GET /api/persons/search/name"
        },
        "audit": {
            "list": "GET /api/audit/",
            "user_logs": "GET /api/audit/user/{user_id}",
            "action_logs": "GET /api/audit/action/{action}",
            "resource_logs": "GET /api/audit/resource/{resource}",
            "stats": "GET /api/audit/stats",
            "recent": "GET /api/audit/recent"
        },
        "system": {
            "health": "GET /api/health",
            "info": "GET /",
            "docs": "GET /api/docs",
            "redoc": "GET /api/redoc",
            "openapi": "GET /api/openapi.json"
        }
    }


def print_system_status():
    """Imprimir estado del sistema en consola"""
    print("=" * 80)
    print("🔒 SISTEMA DE AUDITORÍA DE SOFTWARE - ESTADO ACTUAL")
    print("=" * 80)
    
    status = get_system_status()
    
    print(f"📅 Fecha de verificación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Estado de la API
    if status["api"] == "OPERATIVA":
        print("✅ API FastAPI: OPERATIVA")
        print("   - Documentación: http://localhost:8000/api/docs")
        print("   - Redoc: http://localhost:8000/api/redoc")
        print("   - Health Check: http://localhost:8000/api/health")
    else:
        print(f"❌ API FastAPI: {status['api']}")
    
    print()
    
    # Estado de la base de datos
    if status["database"] == "OPERATIVA":
        print("✅ Base de datos PostgreSQL: OPERATIVA")
        if status["statistics"]:
            print(f"   - Usuarios registrados: {status['statistics']['users']}")
            print(f"   - Personas registradas: {status['statistics']['persons']}")
            print(f"   - Logs de auditoría: {status['statistics']['audit_logs']}")
    else:
        print(f"❌ Base de datos PostgreSQL: {status['database']}")
    
    print()
    
    # Mostrar errores detectados
    if status["errors"]:
        print("⚠️ ERRORES DETECTADOS:")
        for i, error in enumerate(status["errors"], 1):
            print(f"\n   🔴 ERROR #{i}: {error['tipo']}")
            print(f"      - Mensaje: {error['mensaje']}")
            if "detalles" in error:
                print(f"      - Detalles: {error['detalles']}")
            print(f"      - Solución sugerida: {error['solucion']}")
        print()
    
    # Mostrar endpoints disponibles
    print("📋 ENDPOINTS DE LA API DISPONIBLES:")
    endpoints = status["endpoints"]
    
    for category, routes in endpoints.items():
        print(f"\n   🔹 {category.upper()}:")
        for name, path in routes.items():
            print(f"     - {name}: {path}")
    
    print()
    print("=" * 80)
    
    return status


if __name__ == "__main__":
    print_system_status()
