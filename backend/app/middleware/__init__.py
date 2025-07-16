"""
Middleware de la aplicación
"""

from app.middleware.cors import setup_cors

__all__ = ["setup_cors"]
