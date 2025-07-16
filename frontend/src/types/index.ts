// Tipos para la aplicación de auditoría
export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  department: string;
  avatar?: string;
}

export interface Project {
  id: number;
  name: string;
  description: string;
  status: 'Planificado' | 'Iniciando' | 'En Progreso' | 'Revisión' | 'Completado';
  priority: 'Baja' | 'Media' | 'Alta' | 'Crítica';
  progress: number;
  assignedTo: string;
  startDate: string;
  endDate: string;
  riskLevel: 'Bajo' | 'Medio' | 'Alto';
  findings: number;
  budget?: number;
  client?: string;
}

export interface Finding {
  id: number;
  projectId: number;
  title: string;
  description: string;
  severity: 'Bajo' | 'Medio' | 'Alto' | 'Crítico';
  category: 'Seguridad' | 'Funcionalidad' | 'Performance' | 'Usabilidad' | 'Compliance';
  status: 'Abierto' | 'En Progreso' | 'Resuelto' | 'Verificado' | 'Cerrado';
  assignedTo: string;
  dueDate: string;
  createdAt: string;
  updatedAt: string;
}

export interface Report {
  id: number;
  title: string;
  projectId: number;
  type: 'Seguridad' | 'Vulnerabilidades' | 'Cumplimiento' | 'Performance' | 'Funcional';
  status: 'Borrador' | 'En Revisión' | 'Completado' | 'Publicado';
  severity: 'Bajo' | 'Medio' | 'Alto' | 'Crítico';
  findings: number;
  resolved: number;
  author: string;
  createdAt: string;
  publishedAt?: string;
  summary: string;
  recommendations: string[];
}

export interface AuditMetrics {
  totalProjects: number;
  activeProjects: number;
  completedProjects: number;
  totalFindings: number;
  openFindings: number;
  resolvedFindings: number;
  criticalFindings: number;
  averageResolutionTime: number;
}

export interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor: string | string[];
    borderColor?: string;
    borderWidth?: number;
    fill?: boolean;
  }[];
}

export interface NotificationSettings {
  emailReports: boolean;
  pushNotifications: boolean;
  weeklyDigest: boolean;
  criticalAlerts: boolean;
  systemUpdates: boolean;
}

export interface SecuritySettings {
  twoFactorAuth: boolean;
  sessionTimeout: number;
  passwordExpiry: number;
  loginNotifications: boolean;
}

export interface AppearanceSettings {
  theme: 'light' | 'dark' | 'auto';
  language: 'es' | 'en' | 'pt';
  compactMode: boolean;
  animations: boolean;
}

export interface Integration {
  id: number;
  name: string;
  type: string;
  status: 'Conectado' | 'Desconectado' | 'Error';
  lastSync?: string;
  config?: Record<string, any>;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  errors?: string[];
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface FilterOptions {
  status?: string;
  priority?: string;
  severity?: string;
  type?: string;
  assignedTo?: string;
  dateRange?: {
    start: string;
    end: string;
  };
}

export interface DashboardStats {
  activeProjects: number;
  completedAudits: number;
  detectedIssues: number;
  criticalPending: number;
  trends: {
    projectsChange: number;
    auditsChange: number;
    issuesChange: number;
    criticalChange: number;
  };
}

export interface TeamMember {
  id: number;
  name: string;
  email: string;
  role: string;
  department: string;
  avatar?: string;
  activeProjects: number;
  completedProjects: number;
  expertise: string[];
}

export interface AuditTemplate {
  id: number;
  name: string;
  description: string;
  category: string;
  checklist: ChecklistItem[];
  estimatedHours: number;
  requiredSkills: string[];
}

export interface ChecklistItem {
  id: number;
  title: string;
  description: string;
  category: string;
  required: boolean;
  completed: boolean;
  evidence?: string;
  notes?: string;
}

export interface RiskAssessment {
  id: number;
  projectId: number;
  category: string;
  description: string;
  likelihood: 'Muy Baja' | 'Baja' | 'Media' | 'Alta' | 'Muy Alta';
  impact: 'Muy Bajo' | 'Bajo' | 'Medio' | 'Alto' | 'Muy Alto';
  riskLevel: 'Bajo' | 'Medio' | 'Alto' | 'Crítico';
  mitigationPlan: string;
  owner: string;
  dueDate: string;
  status: 'Identificado' | 'Evaluado' | 'Mitigado' | 'Aceptado';
}

export interface ComplianceFramework {
  id: number;
  name: string;
  version: string;
  description: string;
  requirements: ComplianceRequirement[];
  applicableTo: string[];
}

export interface ComplianceRequirement {
  id: number;
  code: string;
  title: string;
  description: string;
  category: string;
  mandatory: boolean;
  evidenceRequired: boolean;
  validationCriteria: string[];
}

export interface Evidence {
  id: number;
  findingId: number;
  type: 'Screenshot' | 'Document' | 'Log' | 'Code' | 'Test Result';
  filename: string;
  description: string;
  uploadedBy: string;
  uploadedAt: string;
  fileSize: number;
  mimeType: string;
  url: string;
}

export interface AuditPlan {
  id: number;
  projectId: number;
  name: string;
  objectives: string[];
  scope: string;
  methodology: string;
  timeline: {
    startDate: string;
    endDate: string;
    phases: AuditPhase[];
  };
  resources: {
    teamMembers: number[];
    tools: string[];
    budget: number;
  };
  deliverables: string[];
  approvedBy: string;
  approvedAt: string;
}

export interface AuditPhase {
  id: number;
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  deliverables: string[];
  dependencies: number[];
  status: 'Pendiente' | 'En Progreso' | 'Completado' | 'Retrasado';
}

export type Priority = 'Baja' | 'Media' | 'Alta' | 'Crítica';
export type Status = 'Planificado' | 'Iniciando' | 'En Progreso' | 'Revisión' | 'Completado';
export type Severity = 'Bajo' | 'Medio' | 'Alto' | 'Crítico';
export type RiskLevel = 'Bajo' | 'Medio' | 'Alto' | 'Crítico';
