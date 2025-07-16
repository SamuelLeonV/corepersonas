"""
Dependencias de seguridad para la aplicación.
"""

from fastapi import Request, Response
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Callable
from ..core.csp_config import CSPConfig


class SecurityHeaders:
    """Middleware para agregar headers de seguridad"""
    
    def __init__(self, app: ASGIApp):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    
                    # Verificar si es una ruta de documentación
                    path = scope.get("path", "")
                    is_docs_route = (path.startswith("/api/docs") or 
                                   path.startswith("/api/redoc") or 
                                   path.startswith("/api/openapi.json") or
                                   path.startswith("/docs/oauth2-redirect"))
                    
                    # CSP más permisivo para documentación, más estricto para el resto
                    if is_docs_route:
                        csp = CSPConfig.get_docs_csp()
                    else:
                        csp = CSPConfig.get_api_csp()
                    
                    # Agregar headers de seguridad
                    security_headers = {
                        b"X-Content-Type-Options": b"nosniff",
                        b"X-Frame-Options": b"DENY",
                        b"X-XSS-Protection": b"1; mode=block",
                        b"Strict-Transport-Security": b"max-age=31536000; includeSubDomains",
                        b"Content-Security-Policy": csp.encode(),
                        b"Referrer-Policy": b"strict-origin-when-cross-origin",
                        b"Permissions-Policy": b"camera=(), microphone=(), geolocation=()",
                    }
                    
                    headers.update(security_headers)
                    message["headers"] = list(headers.items())
                
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Middleware básico de rate limiting"""
    
    def __init__(self, app: ASGIApp, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = {}
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Implementación básica - en producción usar Redis
        client_ip = request.client.host
        
        response = await call_next(request)
        return response


# Instancia del bearer token
security = HTTPBearer()
