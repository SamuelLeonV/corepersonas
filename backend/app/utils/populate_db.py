#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de prueba
"""

import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from app.models import User, Person, AuditLog
from app.core.security_utils import SecurityUtils
from app.core.security_service import SecurityService
from app.db.database import engine
from datetime import datetime, timedelta


# Configurar Faker para español chileno
fake = Faker('es_CL')

# Religiones comunes en Chile
RELIGIONES = [
    "Católica",
    "Evangélica",
    "Testigo de Jehová",
    "Mormón",
    "Judía",
    "Musulmana",
    "Budista",
    "Ateo",
    "Agnóstico",
    "Otra"
]


def generate_valid_rut():
    """Generar un RUT válido chileno"""
    rut_number = random.randint(10000000, 25000000)
    
    # Calcular dígito verificador
    serie = [2, 3, 4, 5, 6, 7]
    sum_value = 0
    rut_str = str(rut_number)
    
    for i in range(len(rut_str)):
        sum_value += int(rut_str[-(i+1)]) * serie[i % len(serie)]
    
    dv = 11 - (sum_value % 11)
    
    if dv == 11:
        dv = '0'
    elif dv == 10:
        dv = 'K'
    else:
        dv = str(dv)
    
    return f"{rut_number}-{dv}"


def create_test_users(db, count: int = 5):
    """Crear usuarios de prueba"""
    print(f"Creando {count} usuarios de prueba...")
    
    created_users = []
    
    for i in range(count):
        email = fake.email()
        
        # Verificar que el email no exista
        if db.query(User).filter(User.email == email).first():
            continue
        
        user = User(
            email=email,
            hashed_password=SecurityUtils.get_password_hash("password123"),
            is_active=True,
            is_admin=i == 0  # Primer usuario es admin
        )
        
        db.add(user)
        created_users.append(user)
    
    db.commit()
    
    for user in created_users:
        db.refresh(user)
    
    print(f"✅ {len(created_users)} usuarios creados")
    return created_users


def create_test_persons(db, users, count: int = 50):
    """Crear personas de prueba"""
    print(f"Creando {count} personas de prueba...")
    
    created_persons = []
    
    for i in range(count):
        # Generar RUT válido
        rut = generate_valid_rut()
        
        # Verificar que el RUT no exista ya encriptado
        rut_hash = SecurityService.hash_rut(rut)
        if db.query(Person).filter(Person.rut_hash == rut_hash).first():
            continue
        
        # Seleccionar religión aleatoria
        religion = random.choice(RELIGIONES)
        religion_hash, salt = SecurityService.hash_religion(religion)
        
        # Encriptar RUT
        encrypted_rut = SecurityService.encrypt_rut(rut)
        
        # Crear persona
        person = Person(
            rut=encrypted_rut,  # RUT encriptado
            rut_hash=rut_hash,  # Hash del RUT para búsquedas
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            religion_hash=religion_hash,
            religion_salt=salt,
            email=fake.email() if random.random() > 0.3 else None,
            telefono=fake.phone_number() if random.random() > 0.4 else None,
            direccion=fake.address() if random.random() > 0.5 else None,
            fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80) if random.random() > 0.2 else None,
            created_by=random.choice(users).id
        )
        
        db.add(person)
        created_persons.append(person)
        created_persons.append(person)
    
    db.commit()
    
    for person in created_persons:
        db.refresh(person)
    
    print(f"✅ {len(created_persons)} personas creadas")
    return created_persons


def create_test_audit_logs(db, users, persons, count: int = 100):
    """Crear logs de auditoría de prueba"""
    print(f"Creando {count} logs de auditoría de prueba...")
    
    actions = ["CREATE", "READ", "UPDATE", "DELETE"]
    resources = ["User", "Person"]
    
    created_logs = []
    
    for i in range(count):
        # Seleccionar datos aleatorios
        user = random.choice(users)
        action = random.choice(actions)
        resource = random.choice(resources)
        
        # Seleccionar recurso específico
        if resource == "Person" and persons:
            resource_id = random.choice(persons).id
        else:
            resource_id = user.id
        
        # Crear log
        log = AuditLog(
            user_id=user.id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=fake.ipv4(),
            user_agent=fake.user_agent(),
            details=f"Acción {action} en {resource} {resource_id}",
            timestamp=fake.date_time_between(start_date="-30d", end_date="now")
        )
        
        db.add(log)
        created_logs.append(log)
    
    db.commit()
    
    print(f"✅ {len(created_logs)} logs de auditoría creados")
    return created_logs


def populate_database(
    users_count: int = 5,
    persons_count: int = 50,
    audit_logs_count: int = 100
):
    """Poblar la base de datos con datos de prueba"""
    print("🗄️  POBLANDO BASE DE DATOS CON DATOS DE PRUEBA")
    print("=" * 60)
    
    # Crear sesión de base de datos
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Crear usuarios de prueba
        users = create_test_users(db, users_count)
        
        # Crear personas de prueba
        persons = create_test_persons(db, users, persons_count)
        
        # Crear logs de auditoría de prueba
        audit_logs = create_test_audit_logs(db, users, persons, audit_logs_count)
        
        print()
        print("✅ Base de datos poblada exitosamente")
        print(f"   - {len(users)} usuarios creados")
        print(f"   - {len(persons)} personas creadas")
        print(f"   - {len(audit_logs)} logs de auditoría creados")
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_test_data():
    """Limpiar todos los datos de prueba"""
    print("🧹 LIMPIANDO DATOS DE PRUEBA")
    print("=" * 60)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Eliminar en orden correcto (por dependencias)
        audit_count = db.query(AuditLog).count()
        persons_count = db.query(Person).count()
        users_count = db.query(User).filter(User.email != "admin@auditoria.com").count()
        
        if audit_count > 0:
            db.query(AuditLog).delete()
            print(f"✅ {audit_count} logs de auditoría eliminados")
        
        if persons_count > 0:
            db.query(Person).delete()
            print(f"✅ {persons_count} personas eliminadas")
        
        if users_count > 0:
            db.query(User).filter(User.email != "admin@auditoria.com").delete()
            print(f"✅ {users_count} usuarios eliminados")
        
        db.commit()
        print("✅ Datos de prueba limpiados exitosamente")
        
    except Exception as e:
        print(f"❌ Error al limpiar datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_test_data()
    else:
        populate_database()
