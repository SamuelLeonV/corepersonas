# Sistema de Auditoría de Software - Frontend

Este proyecto es un sistema de Gestión de Personas con gestión de personas, desarrollado con React y TypeScript.

## Características Principales

- **Gestión de Personas**: CRUD completo con validación de RUT chileno
- **Seguridad**: Ofuscación de datos sensibles y hash irreversible de religión
- **Búsqueda Avanzada**: Por RUT específico y búsqueda general
- **Interfaz Moderna**: Material-UI con animaciones y diseño responsivo
- **Autenticación**: Sistema de login y protección de rutas
- **Auditoría**: Registro de operaciones críticas

## Instalación y Configuración

### 1. Instalar dependencias

```bash
npm install
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

### 3. Ejecutar el proyecto

```bash
npm start
```

El proyecto se abrirá en [http://localhost:3000](http://localhost:3000)

## Configuración de la API

La API del backend se ejecuta en:
```
http://localhost:8000/
```

Para configurar la URL de la API, edita el archivo `.env`:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Scripts Disponibles

En el directorio del proyecto, puedes ejecutar:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Módulos del Sistema

### 📊 Dashboard
- Estadísticas generales del sistema
- Gráficos de actividad
- Resumen de operaciones

### 👥 Gestión de Personas
- CRUD completo con validación de RUT chileno
- Ofuscación de datos sensibles
- Búsqueda por RUT específico
- Ver documentación detallada en: [README_PERSONAS.md](./README_PERSONAS.md)

### 🔐 Autenticación
- Sistema de login/logout
- Protección de rutas
- Manejo de tokens JWT

### 🛡️ Auditoría
- Registro de operaciones críticas
- Logs de acceso y cambios
- Trazabilidad de acciones

## Estructura del Proyecto

```
src/
├── components/          # Componentes reutilizables
│   ├── Auth/           # Componentes de autenticación
│   ├── Forms/          # Formularios (PersonForm, RutSearch, etc.)
│   ├── Layout/         # Layout principal
│   └── UI/             # Componentes de interfaz
├── pages/              # Páginas principales
│   ├── Dashboard/      # Dashboard principal
│   ├── Login/          # Página de login
│   ├── Persons/        # Gestión de personas
│   └── Reports/        # Reportes y auditoría
├── services/           # Servicios de API
├── types/              # Tipos TypeScript
├── contexts/           # Contextos React
└── theme/              # Configuración de tema
```

## Tecnologías Utilizadas

- **React 18**: Framework principal
- **TypeScript**: Tipado estático
- **Material-UI**: Componentes de interfaz
- **React Router**: Navegación
- **React Hook Form**: Manejo de formularios
- **Yup**: Validación de esquemas
- **Framer Motion**: Animaciones
- **Axios**: Cliente HTTP

## Variables de Entorno

```env
# URL base de la API
REACT_APP_API_URL=http://localhost:8000/api

# Entorno de desarrollo
NODE_ENV=development

# Desactivar source maps en producción (opcional)
GENERATE_SOURCEMAP=false
```

## Conexión con la API

### Requisitos Previos

1. **Backend API ejecutándose**: Asegúrate de que la API esté corriendo en `http://localhost:8000`
2. **CORS configurado**: La API debe permitir requests desde `http://localhost:3000`
3. **Endpoints disponibles**: Verifica que los endpoints de personas estén operativos

### Verificar Conexión

Puedes verificar que la API esté funcionando accediendo a:
- `http://localhost:8000/` - Información general del sistema
- `http://localhost:8000/api/persons` - Lista de personas (requiere autenticación)

### Solución de Problemas

**Error de CORS:**
```
Access to fetch at 'http://localhost:8000/api/persons' from origin 'http://localhost:3000' has been blocked by CORS policy
```
**Solución**: Configurar CORS en el backend para permitir requests desde `localhost:3000`

**Error de Conexión:**
```
Network Error: connect ECONNREFUSED 127.0.0.1:8000
```
**Solución**: Verificar que la API esté ejecutándose en el puerto 8000

**Error de Autenticación:**
```
401 Unauthorized
```
**Solución**: Realizar login desde la interfaz para obtener token válido

## Aprender Más

Puedes aprender más en la [documentación de Create React App](https://facebook.github.io/create-react-app/docs/getting-started).

Para aprender React, consulta la [documentación de React](https://reactjs.org/).
