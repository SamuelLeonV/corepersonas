#!/bin/bash
set -e

# Script de inicialización para PostgreSQL
echo "Inicializando base de datos de auditoría..."

# Crear usuario adicional para la aplicación
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Crear esquemas necesarios
    CREATE SCHEMA IF NOT EXISTS audit;
    CREATE SCHEMA IF NOT EXISTS security;
    
    -- Configurar extensiones necesarias
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
    
    -- Crear roles de seguridad
    CREATE ROLE audit_read_only;
    CREATE ROLE audit_read_write;
    
    -- Configurar permisos básicos
    GRANT CONNECT ON DATABASE $POSTGRES_DB TO audit_read_only;
    GRANT CONNECT ON DATABASE $POSTGRES_DB TO audit_read_write;
    
    GRANT USAGE ON SCHEMA public TO audit_read_only, audit_read_write;
    GRANT USAGE ON SCHEMA audit TO audit_read_only, audit_read_write;
    GRANT USAGE ON SCHEMA security TO audit_read_only, audit_read_write;
    
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO audit_read_only;
    GRANT SELECT ON ALL TABLES IN SCHEMA audit TO audit_read_only;
    GRANT SELECT ON ALL TABLES IN SCHEMA security TO audit_read_only;
    
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO audit_read_write;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA audit TO audit_read_write;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA security TO audit_read_write;
    
    -- Configurar permisos por defecto
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO audit_read_only;
    ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT SELECT ON TABLES TO audit_read_only;
    ALTER DEFAULT PRIVILEGES IN SCHEMA security GRANT SELECT ON TABLES TO audit_read_only;
    
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO audit_read_write;
    ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO audit_read_write;
    ALTER DEFAULT PRIVILEGES IN SCHEMA security GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO audit_read_write;
    
    -- Otorgar permisos al usuario principal
    GRANT audit_read_write TO $POSTGRES_USER;
EOSQL

echo "Base de datos inicializada correctamente"
