# Multi-stage Dockerfile para Backend de Auditoría

# Etapa base para dependencias comunes
FROM python:3.11-slim-bullseye AS base

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requirements
COPY requirements.txt ./

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn uvicorn[standard]

# Etapa de desarrollo
FROM base AS development

# Variables de entorno para desarrollo
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=development

# Copiar código fuente
COPY --chown=appuser:appuser . .

# Crear directorios necesarios
RUN mkdir -p /app/logs /tmp && \
    chown -R appuser:appuser /app /tmp

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Etapa de producción
FROM base AS production

# Variables de entorno para producción
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production
ENV PYTHONOPTIMIZE=1

# Copiar solo los archivos necesarios
COPY --chown=appuser:appuser main.py alembic.ini ./
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser alembic/ ./alembic/

# Crear directorios necesarios con permisos restringidos
RUN mkdir -p /app/logs /tmp && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 750 /app/logs

USER appuser

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Comando optimizado para producción
CMD ["gunicorn", "main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "/app/logs/access.log", \
     "--error-logfile", "/app/logs/error.log", \
     "--log-level", "info", \
     "--timeout", "120", \
     "--keep-alive", "5", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100"]

# Etapa para migraciones
FROM base AS migration

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Copiar archivos necesarios para migraciones
COPY --chown=appuser:appuser alembic.ini ./
COPY --chown=appuser:appuser alembic/ ./alembic/
COPY --chown=appuser:appuser app/ ./app/

USER appuser

CMD ["alembic", "upgrade", "head"]
