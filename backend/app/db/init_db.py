"""
Inicialización de la base de datos y utilidades.
"""

from sqlalchemy import create_engine
from app.core.config import settings
from app.db.database import Base, engine


def init_db():
    """Inicializar la base de datos"""
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    

def drop_db():
    """Eliminar todas las tablas"""
    Base.metadata.drop_all(bind=engine)


def reset_db():
    """Resetear la base de datos"""
    drop_db()
    init_db()
