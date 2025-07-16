"""
Middleware para configuración CORS de la aplicación
"""

from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def setup_cors(app):
    """
    Configura el middleware CORS para permitir solicitudes desde orígenes autorizados
    """
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
    
    # Registro en consola
    print(f"✅ CORS configurado con orígenes: {settings.cors_origins_list}")
    print(f"✅ CORS métodos permitidos: TODOS (incluyendo OPTIONS)")
    print(f"✅ CORS cabeceras permitidas: TODAS")
