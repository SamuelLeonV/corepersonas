// Tipos específicos para el sistema de Personas con datos sensibles
export interface Person {
  id: number;
  rut: string; // RUT completo retornado por la API
  rut_masked: string; // RUT ofuscado para mostrar en la UI
  nombre: string;
  apellido: string;
  religion_indicator: string; // Hash irreversible de la religión
  email?: string | null;
  telefono?: string | null;
  direccion?: string | null;
  fecha_nacimiento?: string | null;
  created_at: string;
  updated_at?: string | null;
}

// Respuesta de la API para crear/actualizar personas
export interface PersonCreateResponse {
  rut: string;
  nombre: string;
  apellido: string;
  religion: string;
  email?: string | null;
  telefono?: string | null;
  direccion?: string | null;
  fecha_nacimiento?: string | null;
  id: number;
  rut_masked: string;
  created_at: string;
  updated_at?: string | null;
}

export interface PersonForm {
  rut: string; // RUT en texto plano para el formulario
  nombre: string;
  apellido: string;
  religion: string; // Religión en texto plano para el formulario
  email?: string | null;
  telefono?: string | null;
  direccion?: string | null;
  fecha_nacimiento?: string | null;
}

// Respuesta de la API para crear/actualizar personas
export interface PersonApiResponse {
  success: boolean;
  message: string;
  data?: any | null;
  errors?: string[] | null;
}

// Respuesta paginada de la API para listar personas
export interface PersonsPaginatedResponse {
  items: Person[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface AuthUser {
  id: number;
  email: string;
  nombre?: string;
  apellido?: string;
  role: 'admin' | 'user';
  createdAt: string;
  lastLogin?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  confirmPassword: string;
  nombre?: string;
  apellido?: string;
}

export interface AuthResponse {
  success: boolean;
  token: string;
  user: AuthUser;
  message?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  errors?: string[];
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export interface PersonFilters {
  search?: string;
  sortBy?: 'nombre' | 'apellido' | 'rut' | 'createdAt';
  sortOrder?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

// Configuraciones de seguridad
export interface SecurityConfig {
  enableRutValidation: boolean;
  maxLoginAttempts: number;
  sessionTimeout: number; // en minutos
  passwordMinLength: number;
  requireSpecialChars: boolean;
}

// Estadísticas del sistema
export interface SystemStats {
  totalPersons: number;
  totalUsers: number;
  recentRegistrations: number;
  systemHealth: 'healthy' | 'warning' | 'critical';
}

// Logs de auditoría
export interface AuditLog {
  id: number;
  user_id: number;
  user_email: string;
  action: 'CREATE' | 'READ' | 'UPDATE' | 'DELETE' | 'LOGIN' | 'LOGOUT';
  resource: string;
  resource_id?: number | null;
  details?: string | null;
  ip_address: string;
  user_agent?: string | null;
  timestamp: string;
}

// Respuesta paginada de logs de auditoría
export interface AuditLogsPaginatedResponse {
  items: AuditLog[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

// Validaciones RUT chileno
export interface RutValidation {
  rut: string;
  isValid: boolean;
  formatted: string; // RUT con formato (XX.XXX.XXX-X)
  message?: string;
}

// Opciones de religión (para select)
export interface ReligionOption {
  value: string;
  label: string;
  category?: 'cristianismo' | 'islam' | 'judaismo' | 'budismo' | 'hinduismo' | 'otra' | 'ninguna';
}

export const RELIGION_OPTIONS: ReligionOption[] = [
  { value: 'catolica', label: 'Católica', category: 'cristianismo' },
  { value: 'evangelica', label: 'Evangélica', category: 'cristianismo' },
  { value: 'protestante', label: 'Protestante', category: 'cristianismo' },
  { value: 'ortodoxa', label: 'Ortodoxa', category: 'cristianismo' },
  { value: 'musulmana', label: 'Musulmana', category: 'islam' },
  { value: 'judia', label: 'Judía', category: 'judaismo' },
  { value: 'budista', label: 'Budista', category: 'budismo' },
  { value: 'hindu', label: 'Hindú', category: 'hinduismo' },
  { value: 'testigo_jehova', label: 'Testigo de Jehová', category: 'cristianismo' },
  { value: 'mormon', label: 'Mormón', category: 'cristianismo' },
  { value: 'adventista', label: 'Adventista', category: 'cristianismo' },
  { value: 'bahá\'í', label: 'Bahá\'í', category: 'otra' },
  { value: 'sij', label: 'Sij', category: 'otra' },
  { value: 'otra', label: 'Otra', category: 'otra' },
  { value: 'agnostica', label: 'Agnóstica', category: 'ninguna' },
  { value: 'atea', label: 'Atea', category: 'ninguna' },
  { value: 'ninguna', label: 'Ninguna', category: 'ninguna' },
];

// Exportar tipos del sistema anterior que siguen siendo útiles
export type Priority = 'Baja' | 'Media' | 'Alta' | 'Crítica';
export type Status = 'Activo' | 'Inactivo' | 'Pendiente' | 'Bloqueado';
export type UserRole = 'admin' | 'user' | 'auditor' | 'viewer';

// Tipos adicionales para el estado de la aplicación
export interface AuthState {
  isAuthenticated: boolean;
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

export interface PersonState {
  persons: Person[];
  currentPerson: Person | null;
  loading: boolean;
  error: string | null;
  filters: PersonFilters;
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
