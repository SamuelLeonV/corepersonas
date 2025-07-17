# 🔐 Sistema de Auditoría de Software - Plataforma Completa

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19.1+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9+-blue.svg)](https://typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

Sistema completo de auditoría de software desarrollado para la asignatura **ISI502-313-225031-TLP-AUDITORÍA DE SOFTWARE** - Parte 2. Implementa un sistema de gestión de personas con características avanzadas de seguridad, auditoría y monitoreo.

### 🎯 Características Principales

- 🔐 **Autenticación segura**: Sistema JWT con refresh tokens
- 🔒 **Encriptación de datos**: RUT encriptado (AES-256) y religión hasheada (SHA256+salt)
- ✅ **Validación chilena**: Algoritmo completo de validación de RUT
- 📊 **Auditoría completa**: Registro de todas las operaciones críticas
- 🛡️ **Seguridad avanzada**: CORS, rate limiting, CSP, headers de seguridad
- 🎨 **Interfaz moderna**: React con Material-UI y animaciones
- 📈 **Monitoreo**: Prometheus, Grafana, y métricas en tiempo real
- 🐳 **Despliegue**: Docker y Docker Compose para producción
- 🔄 **CI/CD**: Pipeline automatizado con testing y despliegue

## 🏗️ Arquitectura del Sistema

### 📐 Estructura General

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Frontend    │    │     Backend     │    │    Database     │
│   React + TS    │◄──►│   FastAPI + PY  │◄──►│   PostgreSQL    │
│  Material-UI    │    │   SQLAlchemy    │    │     Redis       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │   Monitoring    │    │    Security     │
│ Reverse Proxy   │    │ Prometheus +    │    │   JWT + AES     │
│   Load Balancer │    │   Grafana       │    │   Validation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔧 Tecnologías Utilizadas

#### Backend (FastAPI)
- **Framework**: FastAPI 0.104+ con OpenAPI/Swagger
- **Base de datos**: PostgreSQL 15 con SQLAlchemy ORM
- **Caché**: Redis 7 para sesiones y rate limiting
- **Seguridad**: JWT, AES-256, bcrypt, Argon2
- **Monitoreo**: Prometheus, Structlog, Loguru
- **Testing**: Pytest con cobertura del 90%+

#### Frontend (React)
- **Framework**: React 19.1+ con TypeScript 4.9+
- **UI Framework**: Material-UI (MUI) v7.2
- **Estado**: React Hook Form + Context API
- **Routing**: React Router DOM v7.6
- **Animaciones**: Framer Motion
- **Gráficos**: Chart.js + React Chart.js 2
- **HTTP Client**: Axios

#### Infraestructura
- **Containerización**: Docker + Docker Compose
- **Reverse Proxy**: Nginx con SSL/TLS
- **Monitoreo**: Prometheus + Grafana + Node Exporter
- **Base de datos**: PostgreSQL + Redis
- **CI/CD**: GitHub Actions (opcional)

## 🚀 Instalación y Configuración

### 📋 Prerrequisitos

- **Docker**: 24.0+ y Docker Compose v2.0+
- **Sistema operativo**: Linux/macOS/Windows con WSL2
- **Memoria**: Mínimo 4GB RAM
- **Almacenamiento**: 10GB espacio libre

### 🔧 Instalación Rápida (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd app
```

2. **Iniciar todos los servicios**
```bash
# Construir y levantar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

3. **Ejecutar migraciones de base de datos**
```bash
# Ejecutar migraciones
docker-compose run --rm migration

# Verificar estado de la base de datos
docker-compose exec postgres psql -U auditoria_user -d auditoria_db -c "\dt"
```

4. **Acceder a la aplicación**
- **Frontend**: [http://localhost:3001](http://localhost:3001)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Documentación API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Grafana**: [http://localhost:3000](http://localhost:3000) (admin/admin_secure_password_2025!)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)

### 🛠️ Instalación para Desarrollo

#### Backend Setup

1. **Navegar al directorio backend**
```bash
cd backend
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tu configuración
```

5. **Ejecutar base de datos con Docker**
```bash
docker-compose up -d postgres redis
```

6. **Ejecutar migraciones**
```bash
alembic upgrade head
```

7. **Iniciar servidor de desarrollo**
```bash
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

1. **Navegar al directorio frontend**
```bash
cd frontend
```

2. **Instalar dependencias**
```bash
npm install
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tu configuración
```

4. **Iniciar servidor de desarrollo**
```bash
npm run dev
```

## 📦 Servicios Docker

URL: http://localhost:xxxx

### 🐳 Servicios Principales

| Servicio | Puerto | Descripción |
|----------|---------|-------------|
| **frontend** | 3001 | Aplicación React con Nginx |
| **backend** | 8000 | API FastAPI con Gunicorn |
| **postgres** | 5432 | Base de datos PostgreSQL |
| **redis** | 6379 | Cache y sesiones |
| **nginx** | 80/443 | Reverse proxy y balanceador |

### 📊 Servicios de Monitoreo

| Servicio | Puerto | Descripción |
|----------|---------|-------------|
| **prometheus** | 9090 | Recolección de métricas |
| **grafana** | 3000 | Dashboard y visualización |
| **node-exporter** | 9100 | Métricas del sistema |
| **postgres-exporter** | 9187 | Métricas de PostgreSQL |
| **redis-exporter** | 9121 | Métricas de Redis |
| **nginx-exporter** | 9113 | Métricas de Nginx |




### 🔐 Credenciales por Defecto Para Demo

```bash
# PostgreSQL
POSTGRES_USER=auditoria_user
POSTGRES_PASSWORD=auditoria_secure_password_2025!
POSTGRES_DB=auditoria_db

# Redis
REDIS_PASSWORD=redis_secure_password_2025!

# Grafana
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin_secure_password_2025!

# JWT
JWT_SECRET=super-secret-jwt-key-for-auditoria-system-2025-change-in-production-a1b2c3d4e5f6g7h8i9j0
```

## 📱 Funcionalidades del Sistema

### 👥 Gestión de Personas

- **CRUD completo**: Crear, leer, actualizar, eliminar personas
- **Validación de RUT**: Algoritmo chileno completo con dígito verificador
- **Encriptación**: RUT encriptado con AES-256, religión hasheada con SHA256+salt
- **Búsqueda avanzada**: Por RUT específico y búsqueda general
- **Paginación**: Resultados paginados para mejor rendimiento

### 🔐 Sistema de Autenticación

- **JWT Tokens**: Access tokens con expiración de 30 minutos
- **Refresh Tokens**: Tokens de actualización con expiración de 7 días
- **Protección de rutas**: Middleware de autenticación
- **Logout seguro**: Invalidación de tokens

### 📊 Auditoría y Logging

- **Registro completo**: Todas las operaciones críticas auditadas
- **Información detallada**: Usuario, timestamp, IP, user-agent
- **Métricas**: Prometheus para monitoreo en tiempo real
- **Logs estructurados**: JSON logs con diferentes niveles

### 🛡️ Seguridad

- **Encriptación**: AES-256 para datos sensibles
- **Hashing**: SHA256 con salt para religión
- **Rate Limiting**: Prevención de ataques de fuerza bruta
- **CORS**: Configuración restrictiva de dominios
- **CSP**: Content Security Policy estricta
- **Headers de seguridad**: HTTPS, HSTS, X-Frame-Options

## 🧪 Testing y Calidad

### 🔍 Backend Testing

```bash
# Ejecutar todos los tests
cd backend
pytest

# Tests con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_auth.py -v
pytest tests/test_persons.py -v
pytest tests/test_audit.py -v
```

### 🎯 Frontend Testing

```bash
# Ejecutar tests unitarios
cd frontend
npm test

# Tests con cobertura
npm run test:coverage

# Tests e2e (si están configurados)
npm run test:e2e
```

### 🌍 Configuración de Producción

1. **Variables de entorno**
```bash
# Actualizar secrets en producción
ENVIRONMENT=production
SECRET_KEY=<generate-secure-key>
DATABASE_URL=<production-database-url>
REDIS_URL=<production-redis-url>
```

2. **SSL/TLS**
```bash
# Configurar certificados SSL
cp your-cert.pem ./docker/nginx/ssl/
cp your-key.pem ./docker/nginx/ssl/
```

3. **Desplegar**
```bash
# Construir imágenes de producción
docker-compose -f docker-compose.yml build

# Iniciar servicios
docker-compose up -d

# Verificar estado
docker-compose ps
```

### 🔄 Comandos Útiles

```bash
# Ver logs de un servicio específico
docker-compose logs -f backend

# Reiniciar un servicio
docker-compose restart frontend

# Ejecutar comando en contenedor
docker-compose exec backend bash

# Backup de base de datos
docker-compose exec postgres pg_dump -U auditoria_user auditoria_db > backup.sql

# Restaurar base de datos
docker-compose exec -T postgres psql -U auditoria_user auditoria_db < backup.sql

# Monitorear recursos
docker-compose exec backend top
```

## 📖 Documentación Adicional

### 📚 API Documentation

- **OpenAPI/Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)


## 🏆 Equipo de Desarrollo

Desarrollado para la asignatura **ISI502-313-225031-TLP-AUDITORÍA DE SOFTWARE** - Parte 2

**Metodología**: Scrum Light con sprints de 2 semanas  
**Periodo**: Julio 2025  
**Institución**: AIEP - Ingeniería en Ejecución

---

*📅 Última actualización: 16 de julio de 2025*
