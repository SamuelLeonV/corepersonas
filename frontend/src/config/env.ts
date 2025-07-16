/**
 * Configuración centralizada de la aplicación
 * Este archivo contiene todas las variables de configuración de la aplicación
 * obtenidas de las variables de entorno
 */

// Configuración de la API
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  TIMEOUT: 10000,
};

// Configuración de autenticación
export const AUTH_CONFIG = {
  TOKEN_KEY: process.env.REACT_APP_AUTH_TOKEN_KEY || 'authToken',
  EXPIRY_KEY: process.env.REACT_APP_AUTH_EXPIRY_KEY || 'authExpiry',
};

// Configuración de la aplicación
export const APP_CONFIG = {
  TITLE: process.env.REACT_APP_TITLE || 'Sistema de Gestión de Personas',
  VERSION: process.env.REACT_APP_VERSION || '1.0.0',
};

// Configuración de características
export const FEATURES_CONFIG = {
  ENABLE_AUDIT: process.env.REACT_APP_ENABLE_AUDIT !== 'false',
  ENABLE_ANALYTICS: process.env.REACT_APP_ENABLE_ANALYTICS === 'true',
};

// Exportar todas las configuraciones juntas para facilitar la importación
const CONFIG = {
  API: API_CONFIG,
  AUTH: AUTH_CONFIG,
  APP: APP_CONFIG,
  FEATURES: FEATURES_CONFIG,
};

export default CONFIG;
