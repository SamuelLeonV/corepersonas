# 📋 GESTIÓN DE TAREAS - TABLERO TRELLO

## 🎯 Configuración del Tablero Principal

### **Nombre del Tablero:** 
`🔐 Sistema Auditoría - Backend API`

### **URL del Tablero:** 
`https://trello.com/b/audit-backend-api`

---

## 📊 ESTRUCTURA DE LISTAS (COLUMNAS)

```
📋 PRODUCT BACKLOG → 🚀 SPRINT BACKLOG → 👨‍💻 IN PROGRESS → 🔍 CODE REVIEW → 🧪 TESTING → ✅ DONE
```

### **1. 📋 PRODUCT BACKLOG**
- **Propósito:** Todas las user stories y tareas pendientes
- **Responsable:** Scrum Master + Product Owner
- **Priorización:** Etiquetas de prioridad + orden en lista

### **2. 🚀 SPRINT BACKLOG** 
- **Propósito:** Tareas comprometidas para el sprint actual
- **Duración:** 2 semanas por sprint
- **Límite WIP:** 25 tareas máximo

### **3. 👨‍💻 IN PROGRESS**
- **Propósito:** Tareas actualmente en desarrollo
- **Límite WIP:** 2 tareas por desarrollador (10 total)
- **Asignación:** Una persona por tarjeta

### **4. 🔍 CODE REVIEW**
- **Propósito:** Pull requests esperando revisión
- **SLA:** Máximo 24 horas para primera revisión
- **Reviewers:** Mínimo 2 aprobaciones requeridas

### **5. 🧪 TESTING**
- **Propósito:** Features completadas esperando QA
- **Responsable:** QA Engineer + desarrollador original
- **Criterios:** Tests automatizados + validación manual

### **6. ✅ DONE**
- **Propósito:** Tareas completamente terminadas
- **Criterios:** Definition of Done cumplida
- **Archive:** Se archivan al final de cada sprint

---

## 🏷️ SISTEMA DE ETIQUETAS

### **🔴 ETIQUETAS DE PRIORIDAD**

| Color | Etiqueta | Descripción | SLA |
|-------|----------|-------------|-----|
| 🔴 | **CRÍTICO** | Bloquea el proyecto completo | < 24h |
| 🟠 | **ALTO** | Importante para el sprint actual | < 3 días |
| 🟡 | **MEDIO** | Puede posponerse al siguiente sprint | < 1 semana |
| 🟢 | **BAJO** | Nice to have, no crítico | Sin SLA |

### **🔵 ETIQUETAS DE TIPO**

| Color | Etiqueta | Descripción |
|-------|----------|-------------|
| 🔵 | **ÉPICA** | Historia de usuario grande |
| 🟣 | **FEATURE** | Nueva funcionalidad |
| 🟤 | **BUG** | Corrección de error |
| ⚫ | **TÉCNICO** | Deuda técnica/refactoring |
| 🔷 | **DOCS** | Documentación |
| 🔶 | **TESTING** | Tareas de QA y testing |

### **🟩 ETIQUETAS DE COMPONENTE**

| Color | Etiqueta | Responsable |
|-------|----------|-------------|
| 🟩 | **AUTH** | Security Engineer |
| 🟦 | **DATABASE** | Database Engineer |
| 🟪 | **API** | API Developer |
| 🟨 | **SECURITY** | Security Engineer |
| 🟫 | **DEVOPS** | Scrum Master/DevOps |
| ⬜ | **QA** | QA Engineer |

---

## 📝 TEMPLATE DE TARJETAS

### **Formato Estándar de Tarjeta:**

```markdown
**TÍTULO:** [TIPO-PRIORIDAD] Descripción breve
**ID:** AUD-001

**📋 DESCRIPCIÓN:**
Como [tipo de usuario]
Quiero [funcionalidad]
Para [beneficio/valor]

**✅ CRITERIOS DE ACEPTACIÓN:**
- [ ] Criterio 1 específico y verificable
- [ ] Criterio 2 con condiciones claras
- [ ] Criterio 3 medible

**🧪 DEFINICIÓN DE TERMINADO:**
- [ ] Código desarrollado y funcionando
- [ ] Tests unitarios escritos y pasando
- [ ] Code review aprobado
- [ ] Documentación actualizada
- [ ] Deploy en ambiente de testing exitoso

**⭐ STORY POINTS:** [1,2,3,5,8,13,21]

**🔗 DEPENDENCIAS:**
- Depende de: #AUD-000
- Bloquea a: #AUD-002

**📎 LINKS:**
- Issue GitHub: #123
- Pull Request: #45
- Branch: feature/auth-system

**📋 SUBTAREAS:**
- [ ] Diseño de API endpoint
- [ ] Implementación de lógica
- [ ] Tests unitarios
- [ ] Documentación
```

---

## 📊 EJEMPLOS DE TARJETAS POR SPRINT

### **SPRINT 1: Fundamentos y Seguridad**

#### **Tarjeta 1:**
```
TÍTULO: [FEATURE-CRÍTICO] Implementar autenticación JWT
ID: AUD-001
COMPONENTE: AUTH
ASIGNADO: Security Engineer
STORY POINTS: 13

DESCRIPCIÓN:
Como administrador del sistema
Quiero un sistema de autenticación seguro con JWT
Para controlar el acceso a la API de auditoría

CRITERIOS DE ACEPTACIÓN:
- [ ] Login con email/password retorna JWT válido
- [ ] JWT expira en 30 minutos configurables
- [ ] Refresh token funcional con expiración extendida
- [ ] Endpoints protegidos validan JWT
- [ ] Logout invalida tokens activos
- [ ] Bloqueo tras 5 intentos fallidos

DEFINICIÓN DE TERMINADO:
- [ ] Endpoints /login, /logout, /refresh funcionando
- [ ] Middleware de autenticación implementado
- [ ] Tests unitarios cobertura > 90%
- [ ] Documentación OpenAPI actualizada
- [ ] Code review aprobado por 2 desarrolladores

SUBTAREAS:
- [ ] Configurar JWT library
- [ ] Crear schemas Pydantic
- [ ] Implementar endpoints auth
- [ ] Crear middleware JWT
- [ ] Tests unitarios
- [ ] Documentación API
```

#### **Tarjeta 2:**
```
TÍTULO: [FEATURE-ALTO] Encriptación reversible de RUT
ID: AUD-002
COMPONENTE: SECURITY
ASIGNADO: Security Engineer
STORY POINTS: 8

DESCRIPCIÓN:
Como desarrollador del sistema
Quiero encriptar RUTs de forma reversible
Para cumplir con requisitos de protección de datos

CRITERIOS DE ACEPTACIÓN:
- [ ] RUT se encripta con AES-256 al guardar
- [ ] Función decrypt devuelve RUT original
- [ ] Salt único por registro
- [ ] Key derivation con PBKDF2
- [ ] Performance < 100ms por operación

DEPENDENCIAS:
- Depende de: AUD-001 (Base auth system)

LINKS:
- Branch: feature/rut-encryption
- Issue: #156
```

### **SPRINT 2: CRUD y Validaciones**

#### **Tarjeta 3:**
```
TÍTULO: [FEATURE-ALTO] CRUD completo de personas
ID: AUD-010
COMPONENTE: API
ASIGNADO: API Developer
STORY POINTS: 13

DESCRIPCIÓN:
Como usuario autenticado
Quiero gestionar información de personas
Para mantener actualizada la base de datos

CRITERIOS DE ACEPTACIÓN:
- [ ] GET /persons con paginación
- [ ] POST /persons crea persona con validaciones
- [ ] PUT /persons/{id} actualiza datos
- [ ] DELETE /persons/{id} elimina registro
- [ ] GET /persons/search/rut busca por RUT
- [ ] Datos sensibles se encriptan automáticamente

SUBTAREAS:
- [ ] Schemas Pydantic para Person
- [ ] Repository pattern para BD
- [ ] Endpoints REST completos
- [ ] Validaciones de entrada
- [ ] Tests de integración
```

#### **Tarjeta 4:**
```
TÍTULO: [FEATURE-MEDIO] Validación RUT chileno
ID: AUD-011  
COMPONENTE: API
ASIGNADO: API Developer
STORY POINTS: 5

DESCRIPCIÓN:
Como sistema
Quiero validar formato y dígito verificador de RUT chileno
Para asegurar calidad de datos

CRITERIOS DE ACEPTACIÓN:
- [ ] Acepta formatos 11.111.111-1 y 11111111-1
- [ ] Valida dígito verificador con algoritmo oficial
- [ ] Rechaza RUTs inválidos con mensaje claro
- [ ] Normaliza formato antes de guardar
```

### **SPRINT 3: Auditoría**

#### **Tarjeta 5:**
```
TÍTULO: [FEATURE-CRÍTICO] Sistema de auditoría completo
ID: AUD-020
COMPONENTE: SECURITY + DATABASE
ASIGNADO: Security Engineer + Database Engineer  
STORY POINTS: 21

DESCRIPCIÓN:
Como auditor del sistema
Quiero registro completo de todas las operaciones
Para cumplir con requisitos de auditoría

CRITERIOS DE ACEPTACIÓN:
- [ ] 17 tipos de acciones auditadas
- [ ] Registro automático en todas las operaciones
- [ ] Información de IP, User-Agent, timestamp
- [ ] No modificable una vez creado
- [ ] Performance no impacta operaciones principales

SUBTAREAS:
- [ ] Modelo AuditLog con campos requeridos
- [ ] Decorator para auto-auditoría  
- [ ] Middleware de captura de datos
- [ ] Endpoints consulta de logs
- [ ] Dashboard básico de auditoría
```

---

## 🎯 GESTIÓN DE SPRINTS EN TRELLO

### **Power-Ups Recomendados:**

1. **📊 Burndown Charts**
   - Tracking de story points por día
   - Velocity del equipo por sprint

2. **⏱️ Time Tracking**
   - Estimación vs tiempo real
   - Productividad por desarrollador

3. **📈 Analytics**
   - Lead time por tipo de tarea
   - Cycle time promedio

4. **🔗 GitHub Integration**
   - Links automáticos a PRs e issues
   - Sincronización de estados

### **Automatizaciones Butler:**

```javascript
// Mover a Testing cuando PR es merged
when a GitHub pull request is merged in card, 
move the card to list "🧪 TESTING"

// Asignar automáticamente por etiqueta
when a card with label "SECURITY" is added to list "👨‍💻 IN PROGRESS",
assign @security-engineer to the card

// Límite WIP en In Progress  
when the number of cards in list "👨‍💻 IN PROGRESS" is greater than 10,
move the oldest card to list "🚀 SPRINT BACKLOG"

// Archivar tareas Done al final de sprint
every friday at 5:00 PM,
archive all cards in list "✅ DONE"
```

---

## 📋 TABLEROS ADICIONALES

### **1. 📊 Tablero de Sprint Planning**
- **Propósito:** Estimación y planning de sprints
- **Listas:** Story Mapping, Estimation, Committed, Overflow

### **2. 🐛 Tablero de Bug Tracking**  
- **Propósito:** Gestión específica de bugs
- **Listas:** Reported, Triaged, In Progress, Fixed, Verified

### **3. 📚 Tablero de Documentación**
- **Propósito:** Tareas de documentación técnica
- **Listas:** To Document, Writing, Review, Published

---

## 📊 MÉTRICAS Y REPORTING

### **KPIs Semanales:**

| Métrica | Target | Actual |
|---------|--------|--------|
| **Story Points Completed** | 40 | 38 |
| **Cycle Time** | <5 días | 4.2 días |
| **Code Review Time** | <24h | 18h |
| **Bug Rate** | <5% | 3% |
| **Test Coverage** | >90% | 92% |

### **Dashboard de Sprint:**

```
🎯 SPRINT 1 - PROGRESO ACTUAL

📊 Story Points: 38/40 (95%)
⏱️ Días restantes: 3
🔥 Burndown: On track
👥 Team velocity: 38 points/sprint

📋 ESTADO POR LISTA:
- Product Backlog: 45 cards
- Sprint Backlog: 2 cards  
- In Progress: 8 cards
- Code Review: 3 cards
- Testing: 4 cards
- Done: 23 cards

⚠️ IMPEDIMENTOS:
- Ambiente de testing inestable (2 días)
- Review de seguridad pendiente (1 día)
```

---

**Este sistema de gestión de tareas en Trello proporciona visibilidad completa, control de flujo de trabajo y métricas para un desarrollo ágil exitoso del sistema de auditoría.**
