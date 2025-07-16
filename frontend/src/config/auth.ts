import { API_CONFIG, AUTH_CONFIG as ENV_AUTH_CONFIG } from './env';

// Configuración de autenticación
export const AUTH_CONFIG = {
  // Claves para localStorage
  TOKEN_KEY: ENV_AUTH_CONFIG.TOKEN_KEY,
  EXPIRY_KEY: ENV_AUTH_CONFIG.EXPIRY_KEY,
  USER_DATA_KEY: 'userData',
  
  
  // Configuración de tokens
  TOKEN_EXPIRY_HOURS: 24,
  
  // Rutas
  LOGIN_ROUTE: '/login',
  DEFAULT_REDIRECT: '/dashboard',
  
  // Configuración de la API
  API_BASE_URL: API_CONFIG.BASE_URL,
  
  // Configuración de seguridad
  SECURITY: {
    // Ocultar RUT (mostrar solo los últimos 4 dígitos)
    RUT_MASK_LENGTH: 4,
    
    // Hash irreversible para religión
    RELIGION_HASH_ALGORITHM: 'SHA-256',
    
    // Configuración de sesión
    SESSION_TIMEOUT_MINUTES: 30,
    
    // Headers de seguridad
    CSRF_TOKEN_HEADER: 'X-CSRF-Token',
    AUTH_HEADER: 'Authorization',
  },
};

// Utilidades de autenticación
export const AuthUtils = {
  // Verificar si el token está expirado
  isTokenExpired: (token: string): boolean => {
    try {
      // Si es el token demo, no expira
      if (token === 'demo-token') return false;
      
      // Para tokens JWT reales, verificar la expiración
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Date.now() / 1000;
      return payload.exp < currentTime;
    } catch {
      return true;
    }
  },
  
  // Obtener datos del usuario desde el token
  getUserFromToken: (token: string): any | null => {
    try {
      if (token === 'demo-token') {
        return {
          id: 'demo-user',
          email: 'admin@auditoria.com',
          name: 'Administrador Demo',
          role: 'admin'
        };
      }
      
      // Para tokens JWT reales
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.user || null;
    } catch {
      return null;
    }
  },
  
  // Ofuscar RUT (mostrar solo los últimos dígitos)
  maskRUT: (rut: string): string => {
    if (!rut || rut.length < AUTH_CONFIG.SECURITY.RUT_MASK_LENGTH) {
      return rut;
    }
    
    const visiblePart = rut.slice(-AUTH_CONFIG.SECURITY.RUT_MASK_LENGTH);
    const hiddenPart = '*'.repeat(rut.length - AUTH_CONFIG.SECURITY.RUT_MASK_LENGTH);
    return hiddenPart + visiblePart;
  },
  
  // Hash irreversible para religión
  hashReligion: async (religion: string): Promise<string> => {
    if (!religion) return '';
    
    try {
      const encoder = new TextEncoder();
      const data = encoder.encode(religion.toLowerCase().trim());
      const hashBuffer = await crypto.subtle.digest('SHA-256', data);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    } catch (error) {
      console.error('Error hashing religion:', error);
      return religion; // Fallback
    }
  },
  
  // Validar RUT chileno
  validateRUT: (rut: string): boolean => {
    if (!rut) return false;
    
    // Limpiar el RUT (eliminar puntos y guiones)
    const cleanRUT = rut.replace(/[.-]/g, '').trim();
    
    // Verificar que el RUT tenga una longitud adecuada
    if (cleanRUT.length < 7 || cleanRUT.length > 9) return false;
    
    // Separar cuerpo y dígito verificador
    const body = cleanRUT.slice(0, -1);
    const dv = cleanRUT.slice(-1).toLowerCase();
    
    // Verificar que el cuerpo contenga solo números
    if (!/^\d+$/.test(body)) return false;
    
    // Verificar que el DV sea un número o 'k'
    if (!/^[0-9k]$/i.test(dv)) return false;
    
    // Calcular dígito verificador
    let sum = 0;
    let multiplier = 2;
    
    for (let i = body.length - 1; i >= 0; i--) {
      sum += parseInt(body[i]) * multiplier;
      multiplier = multiplier === 7 ? 2 : multiplier + 1;
    }
    
    const remainder = sum % 11;
    const calculatedDV = remainder === 0 ? '0' : remainder === 1 ? 'k' : (11 - remainder).toString();
    
    // Comparar el DV calculado con el DV proporcionado
    return dv === calculatedDV;
  },
  
  // Formatear RUT con puntos y guión
  formatRUT: (rut: string): string => {
    if (!rut) return '';
    
    const cleanRUT = rut.replace(/[^0-9kK]/g, '');
    if (cleanRUT.length < 8) return rut;
    
    const body = cleanRUT.slice(0, -1);
    const dv = cleanRUT.slice(-1);
    
    // Agregar puntos cada 3 dígitos
    const formattedBody = body.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    
    return `${formattedBody}-${dv}`;
  },
};

export default AUTH_CONFIG;
