# 📋 METODOLOGÍA DE DESARROLLO - SISTEMA DE AUDITORÍA DE SOFTWARE

## 🚀 METODOLOGÍA ELEGIDA: SCRUM LIGHT

### 🎯 Justificación de la Elección

**¿Por qué Scrum Light en lugar de Kanban?**

#### ✅ **Ventajas de Scrum Light para este proyecto:**

1. **Proyecto con deadline fijo**: Sistema crítico de auditoría con entrega académica definida
2. **Equipo estructurado**: 5 profesionales con roles específicos requieren coordinación clara
3. **Alcance bien definido**: Requisitos de la Parte 2 permiten planificación por sprints
4. **Complejidad técnica**: Seguridad, encriptación y auditoría necesitan iteraciones controladas
5. **Entregables incrementales**: Cada sprint debe producir funcionalidad demostrable
6. **Retrospectivas valiosas**: Importante para mejora continua en equipo académico

#### ❌ **Por qué Kanban sería menos efectivo:**

- No proporciona estructura temporal clara para deadline académico
- Menor control sobre progreso hacia fecha límite
- Menos énfasis en ceremonias de equipo (importantes para coordinación)
- Falta de retrospectivas estructuradas (crítico para aprendizaje)

### 🏗️ **Configuración de Scrum Light**

```
📅 SPRINTS: 2 semanas (14 días)
👥 EQUIPO: 5 profesionales especializados
🎯 CEREMONIAS: Planning, Daily, Review, Retrospective (simplificadas)
📊 ARTEFACTOS: Product Backlog, Sprint Backlog, Increment
🔄 REVISIONES: Code review obligatorio en cada PR
```

---

## 👥 COMPOSICIÓN DEL EQUIPO DE DESARROLLO

### **5 Profesionales Especializados:**

#### 1. **🏆 Scrum Master / DevOps Engineer**
- **Responsabilidades:**
  - Facilitar ceremonias Scrum
  - Configurar CI/CD pipeline
  - Gestionar Docker y despliegue
  - Resolver impedimentos del equipo
- **Skills requeridos:** Git, Docker, CI/CD, metodologías ágiles

#### 2. **🔒 Security Engineer / Backend Lead**
- **Responsabilidades:**
  - Implementar encriptación de datos sensibles
  - Configurar autenticación JWT
  - Realizar auditorías de seguridad
  - Liderar arquitectura backend
- **Skills requeridos:** Python, FastAPI, Cryptography, Security

#### 3. **🗄️ Database Engineer / Backend Developer**
- **Responsabilidades:**
  - Diseñar modelo de base de datos
  - Implementar migraciones con Alembic
  - Optimizar consultas PostgreSQL
  - Desarrollar repositorios y servicios
- **Skills requeridos:** PostgreSQL, SQLAlchemy, Alembic, Python

#### 4. **🔧 API Developer / Integration Specialist**
- **Responsabilidades:**
  - Desarrollar endpoints REST
  - Implementar validaciones de entrada
  - Configurar CORS y middleware
  - Crear documentación OpenAPI
- **Skills requeridos:** FastAPI, Pydantic, REST APIs, Testing

#### 5. **🧪 QA Engineer / Testing Specialist**
- **Responsabilidades:**
  - Crear tests unitarios e integración
  - Validar requisitos de seguridad
  - Realizar testing de carga
  - Documentar casos de prueba
- **Skills requeridos:** pytest, Testing, Security Testing, Documentation

---

## 📅 PLANIFICACIÓN DE SPRINTS

### **Sprint 0: Setup y Configuración (1 semana)**

#### 🎯 **Objetivo:** Preparar entorno de desarrollo y definir estándares

#### **User Stories:**
- **US000-1**: Como equipo, necesitamos configurar el entorno de desarrollo
- **US000-2**: Como equipo, necesitamos definir estándares de código
- **US000-3**: Como equipo, necesitamos configurar repositorio Git

#### **Entregables:**
- ✅ Repositorio Git configurado con branches
- ✅ Docker environment funcional
- ✅ CI/CD pipeline básico
- ✅ Estándares de código definidos

---

### **Sprint 1: Fundamentos y Seguridad (2 semanas)**

#### 🎯 **Objetivo:** Implementar base de datos y autenticación segura

#### **User Stories:**

**US001**: Como desarrollador, quiero una base de datos configurada
- **Criterios de aceptación:**
  - PostgreSQL configurado con Docker
  - Modelos User, Person, AuditLog creados
  - Migraciones Alembic funcionando
- **Estimación:** 8 story points
- **Responsable:** Database Engineer

**US002**: Como admin, quiero autenticación segura
- **Criterios de aceptación:**
  - Login/logout con JWT
  - Refresh tokens implementados
  - Hash de contraseñas con bcrypt
  - Bloqueo tras intentos fallidos
- **Estimación:** 13 story points
- **Responsable:** Security Engineer

**US003**: Como desarrollador, quiero encriptación de RUT
- **Criterios de aceptación:**
  - Encriptación AES-256 reversible
  - Salt único por registro
  - Función decrypt funcional
- **Estimación:** 8 story points
- **Responsable:** Security Engineer

#### **Definición de Terminado Sprint 1:**
- ✅ Autenticación JWT funcional
- ✅ Base de datos con migraciones
- ✅ Encriptación de RUT implementada
- ✅ Tests unitarios > 80% cobertura
- ✅ Code review aprobado
- ✅ Documentación actualizada

---

### **Sprint 2: CRUD y Validaciones (2 semanas)**

#### 🎯 **Objetivo:** Implementar operaciones CRUD y validación de RUT chileno

#### **User Stories:**

**US004**: Como admin, quiero gestionar usuarios
- **Criterios de aceptación:**
  - CRUD completo de usuarios
  - Roles admin/usuario
  - Paginación en listados
- **Estimación:** 8 story points
- **Responsable:** API Developer

**US005**: Como usuario, quiero gestionar personas
- **Criterios de aceptación:**
  - CRUD completo de personas
  - Encriptación automática de datos sensibles
  - Búsqueda por RUT
- **Estimación:** 13 story points
- **Responsable:** API Developer + Database Engineer

**US006**: Como sistema, quiero validar RUT chileno
- **Criterios de aceptación:**
  - Algoritmo dígito verificador correcto
  - Formatos 11.111.111-1 y 11111111-1
  - Mensajes de error claros
- **Estimación:** 5 story points
- **Responsable:** API Developer

#### **Definición de Terminado Sprint 2:**
- ✅ CRUD usuarios y personas completo
- ✅ Validación RUT chileno implementada
- ✅ Endpoints documentados en OpenAPI
- ✅ Tests de integración pasando
- ✅ Validaciones de entrada robustas

---

### **Sprint 3: Auditoría y Seguridad Avanzada (2 semanas)**

#### 🎯 **Objetivo:** Sistema de auditoría completo y features de seguridad

#### **User Stories:**

**US007**: Como auditor, quiero registro de todas las operaciones
- **Criterios de aceptación:**
  - 17 tipos de acciones auditadas
  - IP, User-Agent, timestamp
  - Búsqueda y filtrado de logs
- **Estimación:** 13 story points
- **Responsable:** Security Engineer + Database Engineer

**US008**: Como sistema, quiero hash de religión irreversible
- **Criterios de aceptación:**
  - Hash SHA256 con salt único
  - No reversible por diseño
  - Búsqueda por hash funcional
- **Estimación:** 5 story points
- **Responsable:** Security Engineer

**US009**: Como admin, quiero endpoints de auditoría
- **Criterios de aceptación:**
  - Listado de logs con paginación
  - Estadísticas de auditoría
  - Filtros por fecha, usuario, acción
- **Estimación:** 8 story points
- **Responsable:** API Developer

#### **Definición de Terminado Sprint 3:**
- ✅ Sistema de auditoría 100% funcional
- ✅ Hash de religión implementado
- ✅ Endpoints de auditoría completos
- ✅ Seguridad end-to-end validada

---

### **Sprint 4: Testing y Documentación (2 semanas)**

#### 🎯 **Objetivo:** Testing completo y documentación final

#### **User Stories:**

**US010**: Como QA, quiero testing completo del sistema
- **Criterios de aceptación:**
  - Tests unitarios > 90% cobertura
  - Tests de integración completos
  - Tests de seguridad pasando
- **Estimación:** 13 story points
- **Responsable:** QA Engineer

**US011**: Como usuario, quiero documentación completa
- **Criterios de aceptación:**
  - README.md profesional
  - Guías de instalación y uso
  - Documentación de API actualizada
- **Estimación:** 8 story points
- **Responsable:** QA Engineer + API Developer

**US012**: Como DevOps, quiero deployment automatizado
- **Criterios de aceptación:**
  - Docker Compose funcional
  - Scripts de despliegue
  - Configuración de producción
- **Estimación:** 8 story points
- **Responsable:** Scrum Master/DevOps

#### **Definición de Terminado Sprint 4:**
- ✅ Testing completo y documentado
- ✅ Documentación técnica finalizada
- ✅ Deployment automatizado
- ✅ Proyecto listo para entrega

---

## 🔄 CEREMONIAS SCRUM LIGHT

### 📋 **Sprint Planning** (4 horas cada 2 semanas)
- **Objetivo:** Planificar trabajo del sprint
- **Participantes:** Todo el equipo
- **Entregables:** Sprint backlog comprometido

### 🗣️ **Daily Standup** (15 min, 3 veces/semana)
- **Lunes, Miércoles, Viernes**
- **Preguntas:**
  - ¿Qué completé desde el último daily?
  - ¿Qué planeo completar para el próximo daily?
  - ¿Qué impedimentos tengo?

### 🎯 **Sprint Review** (2 horas)
- **Objetivo:** Demostrar incremento completado
- **Demo funcional** de features desarrolladas
- **Feedback** y ajustes para próximo sprint

### 🔄 **Sprint Retrospective** (1.5 horas)
- **Qué funcionó bien**
- **Qué se puede mejorar**
- **Action items** para próximo sprint

---

## 📊 MÉTRICAS Y SEGUIMIENTO

### **Velocity Tracking**
- Story points completados por sprint
- Burndown charts por sprint
- Tendencia de velocity del equipo

### **Quality Metrics**
- Cobertura de tests (objetivo: >90%)
- Bugs encontrados en testing
- Code review completion rate

### **Team Health**
- Satisfacción del equipo (1-10)
- Impedimentos resueltos vs pendientes
- Time to resolution de blockers

---

**Este plan Scrum Light garantiza entregas incrementales de valor, alta calidad de código y cumplimiento de todos los requisitos de la Parte 2 del sistema de auditoría.**
