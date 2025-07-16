# 🔐 Sistema de Auditoría de Software - Backend API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## 📋 Descripción

API REST segura desarrollada con FastAPI para el sistema de auditoría de software - Parte 2. Implementa autenticación JWT, encriptación de datos sensibles, validación de RUT chileno, y auditoría completa de operaciones.

## ⭐ Características Principales

- 🔐 **Autenticación segura**: JWT con expiración y refresh tokens
- 🔒 **Encriptación de datos**: RUT encriptado (AES-256) y religión hasheada (SHA256+salt)
- ✅ **Validación de RUT chileno**: Algoritmo completo de validación
- 📊 **Auditoría completa**: Registro de todas las operaciones críticas
- 🛡️ **Seguridad**: CORS, rate limiting, validación de entrada, headers de seguridad
- 🗄️ **Base de datos**: PostgreSQL con SQLAlchemy ORM
- 📚 **Documentación**: OpenAPI/Swagger automática

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- PostgreSQL 13+
- pip

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
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
# Editar .env con tus configuraciones
```

5. **Configurar base de datos**
```bash
# Crear base de datos PostgreSQL
createdb auditoria_db

# Ejecutar migraciones
alembic upgrade head
```

6. **Ejecutar aplicación**
```bash
python main.py
```

La API estará disponible en: `http://localhost:8000`

## 🐳 Docker

### Desarrollo con Docker Compose

```bash
docker-compose up -d
```

Esto iniciará:
- Backend API en puerto 8000
- PostgreSQL en puerto 5432
- PgAdmin en puerto 5050

## 📖 Documentación de la API

Una vez ejecutando, accede a:

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI JSON**: `http://localhost:8000/api/openapi.json`

## 🔌 Endpoints Principales

### 🔐 Autenticación (`/api/auth/`)
- `POST /login` - Iniciar sesión
- `POST /register` - Registrar usuario
- `POST /verify-token` - Verificar token
- `POST /refresh` - Renovar token
- `GET /me` - Información del usuario actual

### 👤 Usuarios (`/api/users/`)
- `GET /` - Listar usuarios (admin)
- `POST /` - Crear usuario (admin)
- `GET /{id}` - Obtener usuario
- `PUT /{id}` - Actualizar usuario
- `DELETE /{id}` - Eliminar usuario

### 👥 Personas (`/api/persons/`)
- `GET /` - Listar personas (paginado)
- `POST /` - Crear persona
- `GET /{id}` - Obtener persona
- `PUT /{id}` - Actualizar persona
- `DELETE /{id}` - Eliminar persona
- `GET /search/rut` - Buscar por RUT

### 📊 Auditoría (`/api/audit/`)
- `GET /logs` - Obtener logs de auditoría
- `GET /stats` - Estadísticas de auditoría

## 🔧 Configuración

### Variables de Entorno Principales

```env
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/auditoria_db

# Seguridad
SECRET_KEY=your-super-secret-key-change-in-production
RUT_ENCRYPTION_KEY=your-encryption-key-change-in-production
BCRYPT_ROUNDS=12

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Encriptación
RUT_ENCRYPTION_SALT=your-salt
RUT_ENCRYPTION_ITERATIONS=100000
RELIGION_HASH_ALGORITHM=ARGON2
```

Ver `.env.example` para configuración completa.

## 🗄️ Base de Datos

### Modelos Principales

- **User**: Usuarios del sistema con roles
- **Person**: Personas con datos encriptados
- **AuditLog**: Registro de auditoría

### Migraciones

```bash
# Crear migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1
```

## 🔒 Seguridad Implementada

### 1. **Encriptación de Datos**
- **RUT**: AES-256 reversible con salt
- **Religión**: SHA256 irreversible con salt
- **Contraseñas**: Bcrypt con rounds configurables

### 2. **Autenticación**
- JWT tokens con expiración
- Refresh tokens
- Bloqueo de cuenta tras intentos fallidos

### 3. **Validaciones**
- RUT chileno con dígito verificador
- Email válido
- Sanitización de entrada
- Prevención de inyección SQL

### 4. **Auditoría**
- Registro de todas las operaciones
- Información de IP y User-Agent
- Timestamps precisos
- 17 tipos de acciones auditadas

## 🛠️ Scripts de Utilidad

```bash
# Carga masiva de personas de prueba
python carga_masiva_personas.py

# Verificar encriptación de datos
python fix_unencrypted_data.py

# Probar inserción segura
python test_secure_insertion.py

# Análisis de cumplimiento
python analisis_cumplimiento.py
```

## 📁 Estructura del Proyecto

```
app/
├── api/              # Endpoints REST
│   ├── auth.py       # Autenticación
│   ├── users.py      # Usuarios
│   ├── persons.py    # Personas
│   └── audit.py      # Auditoría
├── core/             # Configuración y seguridad
│   ├── config.py     # Configuración
│   ├── security_service.py  # Servicios de seguridad
│   └── security_utils.py    # Utilidades de seguridad
├── models/           # Modelos SQLAlchemy
│   ├── user.py       # Modelo Usuario
│   ├── person.py     # Modelo Persona
│   └── audit_log.py  # Modelo Auditoría
├── schemas/          # Esquemas Pydantic
├── services/         # Lógica de negocio
├── repositories/     # Acceso a datos
├── utils/            # Utilidades
└── db/              # Base de datos
```

## 🧪 Testing

```bash
# Ejecutar pruebas
python -m pytest

# Pruebas con cobertura
python -m pytest --cov=app

# Pruebas específicas
python test_secure_insertion.py
```

## 📊 Monitoreo y Logs

### Logs de Auditoría
Todas las operaciones críticas se registran con:
- Usuario que realizó la acción
- Tipo de operación
- Recurso afectado
- IP address y User-Agent
- Timestamp preciso
- Detalles adicionales

### Tipos de Acciones Auditadas
- CREATE, READ, UPDATE, DELETE
- LOGIN, LOGOUT, LOGIN_FAILED
- SEARCH, SEARCH_SUCCESS, SEARCH_FAILED
- TOKEN_REFRESH, VERIFY_TOKEN
- REGISTER_USER, PASSWORD_CHANGE

## 🚀 Despliegue

### Producción

1. **Configurar variables de entorno**
```bash
export SECRET_KEY="clave-super-secreta"
export DATABASE_URL="postgresql://user:pass@host/db"
export DEBUG=False
```

2. **Ejecutar con Gunicorn**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

3. **Con Docker**
```bash
docker build -t auditoria-api .
docker run -p 8000:8000 auditoria-api
```

## 📋 Requisitos Cumplidos

✅ **Seguridad**: Encriptación, autenticación, validación  
✅ **Auditoría**: Logging completo de operaciones  
✅ **Base de datos**: Modelo normalizado y optimizado  
✅ **API REST**: Endpoints completos con documentación  
✅ **Validaciones**: RUT chileno, email, datos requeridos  
✅ **Configuración**: Variables de entorno, multi-ambiente  
✅ **Arquitectura**: Servicios, repositorios, middleware  

## 🤝 Contribuir

1. Fork el proyecto
2. Crear branch de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Desarrollador Principal** - *Trabajo inicial* - [Tu Usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM robusto
- Pydantic por la validación de datos
- PostgreSQL por la base de datos confiable

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la [documentación](http://localhost:8000/api/docs)
2. Busca en [Issues](https://github.com/tu-repo/issues)
3. Crea un nuevo [Issue](https://github.com/tu-repo/issues/new)

---

**¡El sistema está listo para producción con todas las funcionalidades de seguridad y auditoría requeridas!** 🚀
