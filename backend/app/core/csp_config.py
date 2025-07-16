"""
Configuración de Content Security Policy (CSP) para la aplicación.
"""

class CSPConfig:
    """Configuración de Content Security Policy"""
    
    # CSP para rutas de documentación (Swagger/ReDoc) - Más permisivo
    DOCS_CSP = {
        "default-src": ["'self'"],
        "script-src": [
            "'self'", 
            "'unsafe-inline'", 
            "'unsafe-eval'",  # Necesario para ReDoc
            "blob:",  # Necesario para Web Workers de ReDoc
            "cdn.jsdelivr.net",
            "unpkg.com",
            "*.unpkg.com",
            "*.jsdelivr.net"
        ],
        "style-src": [
            "'self'", 
            "'unsafe-inline'",
            "fonts.googleapis.com",
            "*.googleapis.com",
            "cdn.jsdelivr.net",
            "*.jsdelivr.net"
        ],
        "font-src": [
            "'self'",
            "fonts.gstatic.com",
            "*.gstatic.com",
            "data:"
        ],
        "img-src": [
            "'self'", 
            "data:",
            "fastapi.tiangolo.com",
            "*.tiangolo.com",
            "cdn.jsdelivr.net",
            "*.jsdelivr.net"
        ],
        "connect-src": ["'self'"],
        "worker-src": [
            "'self'",
            "blob:",  # Necesario para Web Workers de ReDoc
            "cdn.jsdelivr.net",
            "*.jsdelivr.net"
        ],
        "frame-src": ["'none'"],
        "object-src": ["'none'"],
        "base-uri": ["'self'"],
        "form-action": ["'self'"]
    }
    
    # CSP para rutas de API (más restrictivo)
    API_CSP = {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:"],
        "connect-src": ["'self'"],
        "frame-src": ["'none'"],
        "object-src": ["'none'"],
        "base-uri": ["'self'"],
        "form-action": ["'self'"]
    }
    
    @classmethod
    def build_csp_header(cls, csp_config: dict) -> str:
        """Construir header CSP desde configuración"""
        policies = []
        for directive, sources in csp_config.items():
            policy = f"{directive} {' '.join(sources)}"
            policies.append(policy)
        return "; ".join(policies)
    
    @classmethod
    def get_docs_csp(cls) -> str:
        """Obtener CSP para documentación"""
        return cls.build_csp_header(cls.DOCS_CSP)
    
    @classmethod
    def get_api_csp(cls) -> str:
        """Obtener CSP para API"""
        return cls.build_csp_header(cls.API_CSP)
