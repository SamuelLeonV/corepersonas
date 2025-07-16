# 🌿 CONTROL DE VERSIONES - FLUJO GIT ESTÁNDAR

## 📋 Estrategia de Branching

### **Git Flow Simplificado para Equipo de 5 Desarrolladores**

```
main (producción)
├── develop (integración)
    ├── feature/auth-system          (Security Engineer)
    ├── feature/person-crud          (API Developer)
    ├── feature/audit-system         (Security + Database)
    ├── feature/database-setup       (Database Engineer)
    ├── feature/testing-framework    (QA Engineer)
    └── feature/ci-cd-pipeline       (DevOps/Scrum Master)
```

---

## 🚀 FLUJO DE TRABAJO DETALLADO

### **1. Configuración Inicial del Repositorio**

```bash
# Crear repositorio y branches principales
git init
git checkout -b main
git checkout -b develop

# Crear feature branches por desarrollador
git checkout -b feature/auth-system          # Security Engineer
git checkout -b feature/person-crud          # API Developer  
git checkout -b feature/audit-system         # Security + Database
git checkout -b feature/database-setup       # Database Engineer
git checkout -b feature/testing-framework    # QA Engineer
git checkout -b feature/ci-cd-pipeline       # DevOps
```

### **2. Flujo Diario de Desarrollo**

#### **Para cada desarrollador:**

```bash
# 1. Sincronizar con develop
git checkout develop
git pull origin develop

# 2. Crear/actualizar feature branch
git checkout feature/mi-feature
git rebase develop

# 3. Desarrollo local
git add .
git commit -m "feat(auth): implementar JWT authentication"

# 4. Push a feature branch
git push origin feature/mi-feature

# 5. Crear Pull Request
# (Via GitHub/GitLab interface)
```

---

## 📝 CONVENCIÓN DE COMMITS

### **Formato Estándar:**
```
<tipo>(<ámbito>): <descripción>

[cuerpo opcional]

[footer opcional]
```

### **Tipos de Commit:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato, linting
- `refactor`: Refactorización
- `test`: Agregar/modificar tests
- `chore`: Tareas de mantenimiento
- `security`: Cambios de seguridad

### **Ejemplos:**
```bash
feat(auth): implementar autenticación JWT
fix(rut): corregir validación dígito verificador
docs(api): actualizar documentación endpoints
security(encryption): agregar encriptación AES-256
test(person): agregar tests unitarios CRUD
```

---

## 🔍 PULL REQUEST WORKFLOW

### **1. Template de Pull Request**

```markdown
# Pull Request: [FEATURE] Descripción

## 🔍 Descripción
Breve descripción de los cambios realizados.

## 📋 Tipo de cambio
- [ ] 🐛 Bug fix
- [ ] ✨ Nueva funcionalidad  
- [ ] 💥 Breaking change
- [ ] 📚 Documentación
- [ ] 🔒 Seguridad
- [ ] 🧪 Testing

## 🧪 Testing Realizado
- [ ] Tests unitarios pasando
- [ ] Tests de integración pasando
- [ ] Tests de seguridad realizados
- [ ] Tests manuales completados

## 🔒 Checklist de Seguridad
- [ ] Validación de entrada implementada
- [ ] Datos sensibles encriptados/hasheados
- [ ] Logging de auditoría agregado
- [ ] Permisos y roles verificados
- [ ] No hay secrets en código

## 📋 Checklist de Calidad
- [ ] Código cumple estándares del proyecto
- [ ] Documentación actualizada
- [ ] Sin código comentado/debug
- [ ] Variables bien nombradas
- [ ] Funciones con responsabilidad única

## 🔗 Issues relacionadas
Closes #123
Relates to #456

## 📸 Screenshots (si aplica)
[Agregar capturas si hay cambios visuales]

## 👥 Reviewers
@security-engineer @database-engineer
```

### **2. Proceso de Code Review**

#### **Roles de Review por Tipo de Cambio:**

| Tipo de Cambio | Reviewers Requeridos | Aprobaciones Mínimas |
|----------------|---------------------|---------------------|
| **Seguridad** | Security Engineer + 1 más | 2 |
| **Base de Datos** | Database Engineer + 1 más | 2 |
| **API/Backend** | API Developer + 1 más | 2 |
| **Testing** | QA Engineer + 1 más | 2 |
| **DevOps/CI** | Scrum Master + 1 más | 2 |
| **Documentación** | Cualquier 2 miembros | 2 |

#### **Criterios de Review:**

```markdown
### ✅ Code Review Checklist

#### Funcionalidad
- [ ] El código hace lo que debe hacer
- [ ] Los casos edge están cubiertos
- [ ] No hay lógica duplicada

#### Seguridad  
- [ ] Validación de entrada adecuada
- [ ] No hay vulnerabilidades obvias
- [ ] Datos sensibles protegidos

#### Performance
- [ ] No hay consultas N+1
- [ ] Algoritmos eficientes
- [ ] Uso adecuado de caché

#### Mantenibilidad
- [ ] Código legible y bien estructurado
- [ ] Funciones con responsabilidad única
- [ ] Buenos nombres de variables/funciones

#### Testing
- [ ] Tests unitarios incluidos
- [ ] Cobertura adecuada
- [ ] Tests de edge cases
```

---

## 🔧 CONFIGURACIÓN DE HOOKS Y AUTOMATIZACIÓN

### **1. Pre-commit Hooks**

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "🔍 Ejecutando verificaciones pre-commit..."

# Verificar que no se suban archivos sensibles
if git diff --cached --name-only | grep -qE "\.(env|key|pem)$"; then
    echo "❌ Error: Archivos sensibles detectados"
    echo "Archivos problemáticos:"
    git diff --cached --name-only | grep -E "\.(env|key|pem)$"
    exit 1
fi

# Verificar formato de commit
commit_file="$1"
commit_regex='^(feat|fix|docs|style|refactor|test|chore|security)(\(.+\))?: .{1,72}'

if [ -f "$commit_file" ]; then
    if ! head -n1 "$commit_file" | grep -qE "$commit_regex"; then
        echo "❌ Error: Formato de commit inválido"
        echo "Formato correcto: tipo(scope): descripción"
        echo "Ejemplo: feat(auth): implementar login JWT"
        exit 1
    fi
fi

# Ejecutar linting
echo "🔍 Ejecutando linting..."
python -m flake8 app/ || exit 1

# Ejecutar tests rápidos
echo "🧪 Ejecutando tests unitarios..."
python -m pytest tests/unit/ -q || exit 1

echo "✅ Verificaciones pre-commit completadas"
```

### **2. GitHub Actions / GitLab CI**

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.11
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        
    - name: Run linting
      run: |
        flake8 app/
        
    - name: Run security checks
      run: |
        bandit -r app/
        
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
        
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security scan
      uses: securecodewarrior/github-action-add-sarif@v1
      with:
        sarif-file: 'security-scan-results.sarif'
```

---

## 📊 ESTRATEGIA DE RELEASES

### **1. Versionado Semántico**

```
MAYOR.MENOR.PARCHE
1.0.0 → 1.0.1 → 1.1.0 → 2.0.0
```

- **MAYOR**: Cambios incompatibles de API
- **MENOR**: Nueva funcionalidad compatible
- **PARCHE**: Correcciones de bugs

### **2. Release Branches**

```bash
# Crear release branch desde develop
git checkout develop
git checkout -b release/1.0.0

# Finalizar release
git checkout main
git merge release/1.0.0
git tag v1.0.0
git checkout develop  
git merge release/1.0.0
```

### **3. Hotfix Process**

```bash
# Para bugs críticos en producción
git checkout main
git checkout -b hotfix/critical-security-fix
# ... realizar fix ...
git checkout main
git merge hotfix/critical-security-fix
git tag v1.0.1
git checkout develop
git merge hotfix/critical-security-fix
```

---

## 🛡️ POLÍTICAS DE PROTECCIÓN

### **Branch Protection Rules:**

#### **Main Branch:**
- ✅ Require pull request reviews (2 reviewers)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Restrict pushes to admins only
- ✅ Require signed commits

#### **Develop Branch:**
- ✅ Require pull request reviews (1 reviewer)
- ✅ Require status checks to pass
- ✅ Allow force pushes for admins

#### **Feature Branches:**
- ✅ No direct protection
- ✅ Must pass CI/CD pipeline
- ✅ Must be linked to issue/story

---

## 📋 ISSUE TRACKING INTEGRATION

### **Linking Commits to Issues:**

```bash
# Commit que cierra issue
git commit -m "feat(auth): implementar login JWT

Closes #123
Fixes #124"

# Commit que referencia issue
git commit -m "refactor(db): optimizar consultas

Relates to #125"
```

### **Branch Naming Convention:**

```
feature/ISSUE-123-implement-jwt-auth
bugfix/ISSUE-124-fix-rut-validation  
hotfix/ISSUE-125-security-vulnerability
docs/ISSUE-126-update-api-documentation
```

---

**Este flujo Git estándar garantiza código de alta calidad, trazabilidad completa y colaboración efectiva entre los 5 miembros del equipo de desarrollo.**
