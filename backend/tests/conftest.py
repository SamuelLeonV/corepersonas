"""
Configuración para pruebas del sistema de auditoría
"""
import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.database import get_db, Base
from app.routers import auth_router, users_router, persons_router, audit_router
from app.models.user import User
from app.services.user import UserService
from app.schemas.user import UserCreate

# Configuración de base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def create_test_app():
    """Crear aplicación de prueba sin middlewares de seguridad"""
    test_app = FastAPI(title="Test API")
    
    # Solo agregar CORS básico para pruebas
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Incluir routers
    test_app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
    test_app.include_router(users_router, prefix="/api/users", tags=["Usuarios"])
    test_app.include_router(persons_router, prefix="/api/persons", tags=["Personas"])
    test_app.include_router(audit_router, prefix="/api/audit", tags=["Auditoría"])
    
    # Override de dependencias
    test_app.dependency_overrides[get_db] = override_get_db
    
    return test_app


@pytest.fixture(scope="session")
def test_db():
    """Crear base de datos de prueba"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Cliente de prueba para FastAPI sin middlewares de seguridad"""
    test_app = create_test_app()
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def db_session(test_db):
    """Sesión de base de datos para pruebas"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_user_data():
    """Datos de prueba para usuario"""
    return {
        "email": "admin@auditoria.com",
        "full_name": "Test User",
        "password": "Admin123!",  # Contraseña que cumple requisitos de seguridad
        "is_active": True,
        "is_admin": True  # Admin para poder autenticarse en pruebas
    }


@pytest.fixture
def test_person_data():
    """Datos de prueba para persona"""
    return {
        "rut": "99999999-9",  # RUT base que será sobrescrito en tests específicos
        "nombre": "Juan",
        "apellido": "Pérez",
        "religion": "catolica",
        "email": "base@example.com"  # Email base que será sobrescrito
    }


@pytest.fixture
def authenticated_client(client, test_user_data, db_session):
    """Cliente autenticado para pruebas"""
    # Crear usuario directamente en la base de datos usando el servicio
    user_service = UserService(db_session)
    user_create = UserCreate(**test_user_data)
    
    # Verificar si el usuario ya existe, si no, crearlo
    existing_user = user_service.user_repo.get_by_email(test_user_data["email"])
    if existing_user:
        user = existing_user
    else:
        user = user_service.create_user_direct(user_create)
        db_session.commit()
    
    # Autenticar usando el endpoint de login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", json=login_data)
    
    # El login puede devolver 200 o 201 dependiendo de la implementación
    assert response.status_code in [200, 201], f"Login failed with status {response.status_code}: {response.text}"
    
    token = response.json()["access_token"]
    
    # Configurar headers de autenticación para el cliente
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
