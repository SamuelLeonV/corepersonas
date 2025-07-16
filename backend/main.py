"""
ARCHIVO PRINCIPAL - SISTEMA DE AUDITORÍA DE SOFTWARE
===================================================

Este archivo implementa la aplicación principal FastAPI.
Se encarga de inicializar los componentes, configurar middlewares y rutas.
"""

import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge
import psutil

# Asegurar que el path esté configurado
sys.path.insert(0, str(Path(__file__).parent))

# Importar configuraciones y componentes
from app.core.config import settings
from app.api import auth_router, users_router, persons_router, audit_router

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Permitimos todos los métodos, incluyendo OPTIONS
    allow_headers=["*"],  # Permitimos todas las cabeceras
    expose_headers=["*"],
    max_age=600,  # Tiempo en segundos que el navegador puede cachear la respuesta preflight
)

# Configurar instrumentación de Prometheus
print("🔧 Configurando instrumentación de Prometheus...")
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=False,  # Siempre habilitar métricas
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/api/health"],  # Solo excluir endpoint de salud
    inprogress_name="fastapi_inprogress",
    inprogress_labels=True,
)

# Instrumentar la aplicación
print("🔧 Instrumentando aplicación...")
instrumentator.instrument(app)

# Exponer métricas en el endpoint /metrics
print("🔧 Exponiendo endpoint /metrics...")
instrumentator.expose(app, endpoint="/metrics")
print("✅ Instrumentación de Prometheus configurada en /metrics")

# Crear métricas personalizadas del sistema
cpu_usage_gauge = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
memory_usage_gauge = Gauge('system_memory_usage_percent', 'Memory usage percentage')
disk_usage_gauge = Gauge('system_disk_usage_percent', 'Disk usage percentage')

def update_system_metrics():
    """Actualizar métricas del sistema"""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_usage_gauge.set(cpu_percent)
        
        # Memoria
        memory = psutil.virtual_memory()
        memory_usage_gauge.set(memory.percent)
        
        # Disco
        disk = psutil.disk_usage('/')
        disk_usage_gauge.set(disk.percent)
    except Exception as e:
        print(f"⚠️ Error actualizando métricas del sistema: {e}")

# Actualizar métricas del sistema al inicio
update_system_metrics()
print("📊 Métricas del sistema inicializadas")

# Middleware para actualizar métricas del sistema
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware para actualizar métricas del sistema en cada request"""
    # Actualizar métricas del sistema cada 10 requests (para no sobrecargar)
    import random
    if random.randint(1, 10) == 1:
        update_system_metrics()
    
    response = await call_next(request)
    return response

# Registro en consola de la configuración CORS
print(f"✅ CORS configurado con orígenes: {settings.cors_origins_list}")
print(f"✅ CORS métodos permitidos: TODOS (incluyendo OPTIONS)")
print(f"✅ CORS cabeceras permitidas: TODAS")

# Montar los routers en la aplicación
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(users_router, prefix="/api/users", tags=["Usuarios"])
app.include_router(persons_router, prefix="/api/persons", tags=["Personas"])
app.include_router(audit_router, prefix="/api/audit", tags=["Auditoría"])

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones no controladas"""
    # Registrar el error
    print(f"❌ Error no controlado: {str(exc)}")
    import traceback
    traceback.print_exc()
    # Devolver respuesta amigable
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor. El administrador ha sido notificado."}
    )

@app.get("/api/health", tags=["Sistema"])
async def health_check():
    """Endpoint para verificar que la API está funcionando"""
    import time
    
    # Actualizar métricas del sistema para Prometheus
    update_system_metrics()
    
    return {
        "status": "ok", 
        "version": settings.APP_VERSION,
        "timestamp": int(time.time()),
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent if psutil.disk_usage('/') else None
        }
    }

@app.get("/api/metrics-info", tags=["Sistema"])
async def metrics_info():
    """Endpoint que proporciona información sobre las métricas disponibles"""
    return {
        "metrics_endpoint": "/metrics",
        "description": "Métricas de Prometheus para monitoreo",
        "available_metrics": [
            "fastapi_requests_total",
            "fastapi_request_duration_seconds",
            "fastapi_requests_inprogress",
            "fastapi_request_size_bytes",
            "fastapi_response_size_bytes",
            "process_cpu_seconds_total",
            "process_memory_bytes"
        ]
    }

@app.get("/", tags=["Sistema"])
async def root():
    """Endpoint raíz que redirecciona a la documentación"""
    return {"message": "Sistema de Auditoría de Software", 
            "documentation": "/api/docs",
            "version": settings.APP_VERSION}

# Exportar la aplicación para uvicorn
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    print("🚀 Ejecutando aplicación desde main.py")
    print(f"   API: http://{settings.HOST}:{settings.PORT}")
    print(f"   Documentación: http://{settings.HOST}:{settings.PORT}/api/docs")
    print(f"   Redoc: http://{settings.HOST}:{settings.PORT}/api/redoc")
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
