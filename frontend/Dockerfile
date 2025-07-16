# Multi-stage Dockerfile para Frontend React

# Etapa de construcción
FROM node:20-alpine AS builder

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apk add --no-cache \
    git \
    python3 \
    make \
    g++

# Copiar archivos de dependencias
COPY frontend/package.json frontend/package-lock.json* ./

# Instalar todas las dependencias (incluyendo dev para build)
RUN npm ci && npm cache clean --force

# Copiar código fuente del frontend
COPY frontend/ .

# Variables de entorno para construcción
ENV NODE_ENV=production
ENV REACT_APP_API_URL=/api/v1
ENV GENERATE_SOURCEMAP=false

# Construir la aplicación
RUN npm run build

# Etapa de producción con Nginx
FROM nginx:1.25-alpine AS production

# Instalar curl para healthcheck
RUN apk add --no-cache curl

# Copiar archivos construidos desde la etapa anterior
COPY --from=builder /app/build /usr/share/nginx/html

# Copiar configuración de Nginx
COPY docker/nginx/frontend.conf /etc/nginx/conf.d/default.conf

# Configurar permisos
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Exponer puerto
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]

# Etapa de desarrollo
FROM node:20-alpine AS development

WORKDIR /app

# Instalar dependencias del sistema
RUN apk add --no-cache git python3 make g++

# Crear usuario no-root para desarrollo
RUN addgroup -g 1001 -S appuser && \
    adduser -S -D -H -u 1001 -h /app -s /bin/sh -G appuser appuser

# Copiar archivos de dependencias
COPY --chown=appuser:appuser package.json package-lock.json* ./

# Instalar todas las dependencias (incluyendo dev)
RUN npm ci

# Copiar código fuente
COPY --chown=appuser:appuser . .

# Configurar usuario
USER appuser

# Variables de entorno para desarrollo
ENV NODE_ENV=development
ENV REACT_APP_API_URL=http://localhost:8000/api/v1
ENV CHOKIDAR_USEPOLLING=true

EXPOSE 3000

CMD ["npm", "start"]
