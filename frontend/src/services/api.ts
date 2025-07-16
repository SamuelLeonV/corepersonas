import axios, { AxiosResponse } from 'axios';
import { ApiResponse, PaginatedResponse } from '../types';
import { API_CONFIG, AUTH_CONFIG } from '../config/env';

// Configuración base de Axios usando la configuración centralizada
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: API_CONFIG.TIMEOUT,
});

// Interceptor para agregar token de autenticación
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(AUTH_CONFIG.TOKEN_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
      localStorage.removeItem(AUTH_CONFIG.EXPIRY_KEY);
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Servicios de API
export const authService = {
  login: async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      // La API devuelve directamente { access_token, token_type }
      return {
        success: true,
        data: response.data,
        message: 'Login exitoso'
      };
    } catch (error: any) {
      return {
        success: false,
        data: null,
        message: error.response?.data?.detail || 'Error de autenticación'
      };
    }
  },

  register: async (email: string, password: string, name: string): Promise<ApiResponse<{ token: string; user: any }>> => {
    const response = await apiClient.post('/auth/register', { email, password, name });
    return response.data;
  },

  logout: async (): Promise<ApiResponse<null>> => {
    const response = await apiClient.post('/auth/logout');
    return response.data;
  },

  refreshToken: async (): Promise<ApiResponse<{ token: string }>> => {
    const response = await apiClient.post('/auth/refresh');
    return response.data;
  },

  resetPassword: async (email: string): Promise<ApiResponse<null>> => {
    const response = await apiClient.post('/auth/reset-password', { email });
    return response.data;
  },
};

export const projectService = {
  getProjects: async (params?: any): Promise<PaginatedResponse<any>> => {
    const response = await apiClient.get('/projects', { params });
    return response.data;
  },

  getProject: async (id: number): Promise<ApiResponse<any>> => {
    const response = await apiClient.get(`/projects/${id}`);
    return response.data;
  },

  createProject: async (project: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.post('/projects', project);
    return response.data;
  },

  updateProject: async (id: number, project: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.put(`/projects/${id}`, project);
    return response.data;
  },

  deleteProject: async (id: number): Promise<ApiResponse<null>> => {
    const response = await apiClient.delete(`/projects/${id}`);
    return response.data;
  },

  getProjectFindings: async (projectId: number): Promise<ApiResponse<any[]>> => {
    const response = await apiClient.get(`/projects/${projectId}/findings`);
    return response.data;
  },

  getProjectReports: async (projectId: number): Promise<ApiResponse<any[]>> => {
    const response = await apiClient.get(`/projects/${projectId}/reports`);
    return response.data;
  },
};

export const findingService = {
  getFindings: async (params?: any): Promise<PaginatedResponse<any>> => {
    const response = await apiClient.get('/findings', { params });
    return response.data;
  },

  getFinding: async (id: number): Promise<ApiResponse<any>> => {
    const response = await apiClient.get(`/findings/${id}`);
    return response.data;
  },

  createFinding: async (finding: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.post('/findings', finding);
    return response.data;
  },

  updateFinding: async (id: number, finding: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.put(`/findings/${id}`, finding);
    return response.data;
  },

  deleteFinding: async (id: number): Promise<ApiResponse<null>> => {
    const response = await apiClient.delete(`/findings/${id}`);
    return response.data;
  },

  uploadEvidence: async (findingId: number, file: File): Promise<ApiResponse<any>> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('findingId', findingId.toString());

    const response = await apiClient.post('/findings/evidence', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const reportService = {
  getReports: async (params?: any): Promise<PaginatedResponse<any>> => {
    const response = await apiClient.get('/reports', { params });
    return response.data;
  },

  getReport: async (id: number): Promise<ApiResponse<any>> => {
    const response = await apiClient.get(`/reports/${id}`);
    return response.data;
  },

  createReport: async (report: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.post('/reports', report);
    return response.data;
  },

  updateReport: async (id: number, report: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.put(`/reports/${id}`, report);
    return response.data;
  },

  deleteReport: async (id: number): Promise<ApiResponse<null>> => {
    const response = await apiClient.delete(`/reports/${id}`);
    return response.data;
  },

  generateReport: async (projectId: number, template: string): Promise<ApiResponse<any>> => {
    const response = await apiClient.post(`/reports/generate`, { projectId, template });
    return response.data;
  },

  exportReport: async (reportId: number, format: 'pdf' | 'xlsx' | 'docx'): Promise<Blob> => {
    const response = await apiClient.get(`/reports/${reportId}/export`, {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },
};

export const dashboardService = {
  getStats: async (): Promise<ApiResponse<any>> => {
    const response = await apiClient.get('/dashboard/stats');
    return response.data;
  },

  getChartData: async (type: string, period: string): Promise<ApiResponse<any>> => {
    const response = await apiClient.get(`/dashboard/charts/${type}`, {
      params: { period },
    });
    return response.data;
  },

  getRecentActivity: async (limit: number = 10): Promise<ApiResponse<any[]>> => {
    const response = await apiClient.get('/dashboard/activity', {
      params: { limit },
    });
    return response.data;
  },
};

export const userService = {
  getCurrentUser: async (): Promise<ApiResponse<any>> => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  updateProfile: async (profile: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.put('/users/profile', profile);
    return response.data;
  },

  changePassword: async (currentPassword: string, newPassword: string): Promise<ApiResponse<null>> => {
    const response = await apiClient.post('/users/change-password', {
      currentPassword,
      newPassword,
    });
    return response.data;
  },

  getNotificationSettings: async (): Promise<ApiResponse<any>> => {
    const response = await apiClient.get('/users/notifications');
    return response.data;
  },

  updateNotificationSettings: async (settings: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.put('/users/notifications', settings);
    return response.data;
  },

  uploadAvatar: async (file: File): Promise<ApiResponse<any>> => {
    const formData = new FormData();
    formData.append('avatar', file);

    const response = await apiClient.post('/users/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const teamService = {
  getTeamMembers: async (): Promise<ApiResponse<any[]>> => {
    const response = await apiClient.get('/team');
    return response.data;
  },

  inviteTeamMember: async (email: string, role: string): Promise<ApiResponse<any>> => {
    const response = await apiClient.post('/team/invite', { email, role });
    return response.data;
  },

  updateTeamMember: async (id: number, updates: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.put(`/team/${id}`, updates);
    return response.data;
  },

  removeTeamMember: async (id: number): Promise<ApiResponse<null>> => {
    const response = await apiClient.delete(`/team/${id}`);
    return response.data;
  },
};

export const integrationService = {
  getIntegrations: async (): Promise<ApiResponse<any[]>> => {
    const response = await apiClient.get('/integrations');
    return response.data;
  },

  createIntegration: async (integration: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.post('/integrations', integration);
    return response.data;
  },

  updateIntegration: async (id: number, integration: any): Promise<ApiResponse<any>> => {
    const response = await apiClient.put(`/integrations/${id}`, integration);
    return response.data;
  },

  deleteIntegration: async (id: number): Promise<ApiResponse<null>> => {
    const response = await apiClient.delete(`/integrations/${id}`);
    return response.data;
  },

  testIntegration: async (id: number): Promise<ApiResponse<any>> => {
    const response = await apiClient.post(`/integrations/${id}/test`);
    return response.data;
  },

  syncIntegration: async (id: number): Promise<ApiResponse<any>> => {
    const response = await apiClient.post(`/integrations/${id}/sync`);
    return response.data;
  },
};

// Servicio de auditoría
export const auditService = {
  // Ruta principal de auditoría - Lista paginada de logs
  getLogs: async (params?: {
    page?: number;
    per_page?: number;
    action?: string;
    resource?: string;
    user_id?: number;
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await apiClient.get('/audit', { params });
    return response.data;
  },

  // Rutas legacy mantenidas para compatibilidad
  getLogsLegacy: async (params?: {
    skip?: number;
    limit?: number;
    action?: string;
    resource?: string;
    user_id?: number;
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await apiClient.get('/audit/logs', { params });
    return response.data;
  },

  getStats: async (days: number = 30) => {
    try {
      const response = await apiClient.get('/audit/stats', { params: { days } });
      
      // Usar directamente la estructura de la respuesta que vimos en la API real
      const data = response.data;
      
      // Comprobar que todas las propiedades necesarias existen
      const formattedData = {
        actions_by_type: data.actions_by_type || {},
        daily_actions: data.daily_actions || [],
        hourly_distribution: data.hourly_distribution || [],
        resources_by_type: data.resources_by_type || {},
        total_actions: data.total_actions || 0,
        period_days: data.period_days || days,
        most_active_users: data.most_active_users || [],
        frequent_ips: data.frequent_ips || []
      };
      
      console.log('Estadísticas recibidas de la API:', data);
      return formattedData;
    } catch (error) {
      console.error('Error al obtener estadísticas de auditoría:', error);
      // Devolver un objeto con estructura consistente en caso de error
      return {
        actions_by_type: {},
        daily_actions: [],
        hourly_distribution: [],
        resources_by_type: {},
        total_actions: 0,
        period_days: days,
        most_active_users: [],
        frequent_ips: []
      };
    }
  },

  getAvailableActions: async () => {
    const response = await apiClient.get('/audit/actions');
    return response.data;
  },

  getAvailableResources: async () => {
    const response = await apiClient.get('/audit/resources');
    return response.data;
  },

  exportLogs: async (params?: {
    format?: 'csv' | 'json';
    start_date?: string;
    end_date?: string;
    action?: string;
    resource?: string;
  }): Promise<Blob> => {
    const response = await apiClient.get('/audit/export', {
      params: {
        format: 'csv',
        ...params,
      },
      responseType: 'blob',
    });
    return response.data;
  },
};

// Servicio para el CRUD de personas
export const personService = {
  // Listar personas - Ruta principal con paginación
  getPersons: async (params?: {
    page?: number;
    per_page?: number;
    search?: string;
  }) => {
    const response = await apiClient.get('/persons', { params });
    // Normalizar respuesta para manejar formatos inconsistentes
    const data = response.data;
    
    // Normalizar el formato de items si viene como [array, totalCount]
    if (Array.isArray(data.items) && Array.isArray(data.items[0])) {
      return {
        ...data,
        items: data.items[0]  // Extraer el array real de personas
      };
    }
    
    return data;
  },

  // Obtener persona específica por ID
  getPerson: async (id: number) => {
    const response = await apiClient.get(`/persons/${id}`);
    const data = response.data;
    
    // Normalizar respuesta si viene como array
    if (Array.isArray(data)) {
      return data[0]; // Devolver el primer elemento
    }
    
    return data;
  },

  // Crear nueva persona
  createPerson: async (person: {
    rut: string;
    nombre: string;
    apellido: string;
    religion: string;
    email?: string | null;
    telefono?: string | null;
    direccion?: string | null;
    fecha_nacimiento?: string | null;
  }) => {
    try {
      // Procesar datos antes de enviar
      const processedPerson = {
        ...person,
        // Convertir fecha a formato ISO si existe
        fecha_nacimiento: person.fecha_nacimiento ? 
          new Date(person.fecha_nacimiento).toISOString() : null,
        // Asegurar que los campos opcionales sean null si están vacíos
        email: person.email || null,
        telefono: person.telefono || null,
        direccion: person.direccion || null,
      };
      
      const response = await apiClient.post('/persons', processedPerson);
      
      // Verificar si la respuesta contiene el campo id, lo que indica creación exitosa
      if (response.data && response.data.id) {
        return {
          success: true,
          data: response.data,
          message: 'Persona creada con éxito'
        };
      } else {
        // Si no hay id pero hay datos, probablemente se creó pero el formato de respuesta es diferente
        return {
          success: true,
          data: response.data,
          message: 'Persona creada con éxito'
        };
      }
    } catch (error: any) {
      // Manejar errores específicamente
      console.error('Error al crear persona:', error);
      return {
        success: false,
        data: null,
        message: error.response?.data?.detail || 'Error al crear la persona',
        errors: error.response?.data?.errors || null
      };
    }
  },

  // Actualizar persona existente
  updatePerson: async (id: number, person: {
    rut?: string | null;
    nombre?: string | null;
    apellido?: string | null;
    religion?: string | null;
    email?: string | null;
    telefono?: string | null;
    direccion?: string | null;
    fecha_nacimiento?: string | null;
  }) => {
    try {
      // Procesar datos antes de enviar
      const processedPerson = {
        ...person,
        // Convertir fecha a formato ISO si existe
        fecha_nacimiento: person.fecha_nacimiento ? 
          new Date(person.fecha_nacimiento).toISOString() : null,
        // Asegurar que los campos opcionales sean null si están vacíos
        email: person.email || null,
        telefono: person.telefono || null,
        direccion: person.direccion || null,
      };
      
      const response = await apiClient.put(`/persons/${id}`, processedPerson);
      
      // Verificar si la respuesta contiene el campo updated_at, lo que indica una actualización exitosa
      if (response.data && response.data.updated_at) {
        return {
          success: true,
          data: response.data,
          message: 'Persona actualizada con éxito'
        };
      } else {
        // Si no hay updated_at pero hay datos, probablemente se actualizó pero el formato de respuesta es diferente
        return {
          success: true,
          data: response.data,
          message: 'Persona actualizada con éxito'
        };
      }
    } catch (error: any) {
      // Manejar errores específicamente
      console.error('Error al actualizar persona:', error);
      return {
        success: false,
        data: null,
        message: error.response?.data?.detail || 'Error al actualizar la persona',
        errors: error.response?.data?.errors || null
      };
    }
  },

  // Eliminar persona
  deletePerson: async (id: number) => {
    try {
      const response = await apiClient.delete(`/persons/${id}`);
      return {
        success: true,
        data: response.data,
        message: 'Persona eliminada con éxito'
      };
    } catch (error: any) {
      console.error('Error al eliminar persona:', error);
      return {
        success: false,
        data: null,
        message: error.response?.data?.detail || 'Error al eliminar la persona',
        errors: error.response?.data?.errors || null
      };
    }
  },

  // Búsqueda de personas por RUT chileno
  searchPersonByRut: async (rut: string) => {
    const response = await apiClient.get('/persons/search/rut', { params: { rut } });
    return response.data;
  },

  // Búsqueda de personas por nombre y/o apellido
  searchPersonByName: async (params: {
    nombre?: string | null;
    apellido?: string | null;
    page?: number;
    per_page?: number;
  }) => {
    const response = await apiClient.get('/persons/search/name', { params });
    return response.data;
  },

  // Obtener personas creadas por el usuario actual
  getMyPersons: async (params?: {
    page?: number;
    per_page?: number;
  }) => {
    const response = await apiClient.get('/persons/my-persons', { params });
    return response.data;
  },

  // Búsqueda general de personas (mantener para compatibilidad)
  searchPersons: async (query: string) => {
    const response = await apiClient.get('/persons', { params: { search: query } });
    return response.data;
  },
};

// Utility functions
export const downloadFile = (blob: Blob, filename: string) => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export default apiClient;
