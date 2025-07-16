#!/usr/bin/env python3
"""
Utilidades para testing del sistema de auditoría
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional


class APITester:
    """Clase para testear la API del sistema"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Iniciar sesión y obtener token"""
        response = self.session.post(
            f"{self.base_url}/api/auth/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": response.text}
    
    def test_health(self) -> Dict[str, Any]:
        """Testear endpoint de salud"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else None,
                "error": response.text if response.status_code != 200 else None
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_auth_endpoints(self) -> Dict[str, Any]:
        """Testear endpoints de autenticación"""
        results = {}
        
        # Test login
        login_result = self.login("admin@auditoria.com", "admin123")
        results["login"] = login_result
        
        if login_result["success"]:
            # Test me endpoint
            try:
                response = self.session.get(f"{self.base_url}/api/auth/me")
                results["me"] = {
                    "success": response.status_code == 200,
                    "data": response.json() if response.status_code == 200 else None
                }
            except Exception as e:
                results["me"] = {"success": False, "error": str(e)}
        
        return results
    
    def test_persons_endpoints(self) -> Dict[str, Any]:
        """Testear endpoints de personas"""
        if not self.token:
            return {"error": "No hay token de autenticación"}
        
        results = {}
        
        # Test listar personas
        try:
            response = self.session.get(f"{self.base_url}/api/persons/")
            results["list_persons"] = {
                "success": response.status_code == 200,
                "data": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            results["list_persons"] = {"success": False, "error": str(e)}
        
        # Test crear persona (datos de prueba)
        test_person = {
            "rut": "12345678-9",
            "nombre": "Test",
            "apellido": "User",
            "religion": "Católica",
            "email": "test@example.com"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/persons/",
                json=test_person
            )
            results["create_person"] = {
                "success": response.status_code == 201,
                "data": response.json() if response.status_code == 201 else None
            }
        except Exception as e:
            results["create_person"] = {"success": False, "error": str(e)}
        
        return results
    
    def test_audit_endpoints(self) -> Dict[str, Any]:
        """Testear endpoints de auditoría"""
        if not self.token:
            return {"error": "No hay token de autenticación"}
        
        results = {}
        
        # Test listar logs de auditoría
        try:
            response = self.session.get(f"{self.base_url}/api/audit/logs")
            results["list_audit_logs"] = {
                "success": response.status_code == 200,
                "data": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            results["list_audit_logs"] = {"success": False, "error": str(e)}
        
        return results
    
    def run_full_test(self) -> Dict[str, Any]:
        """Ejecutar todas las pruebas"""
        print("🧪 Ejecutando pruebas completas del sistema...")
        print("=" * 60)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "health": self.test_health(),
            "auth": self.test_auth_endpoints(),
            "persons": self.test_persons_endpoints(),
            "audit": self.test_audit_endpoints()
        }
        
        # Imprimir resultados
        self._print_results(results)
        
        return results
    
    def _print_results(self, results: Dict[str, Any]):
        """Imprimir resultados de las pruebas"""
        print(f"📅 Timestamp: {results['timestamp']}")
        print()
        
        # Health check
        health = results["health"]
        if health["success"]:
            print("✅ Health Check: PASSED")
        else:
            print(f"❌ Health Check: FAILED - {health.get('error', 'Unknown error')}")
        
        # Autenticación
        auth = results["auth"]
        if auth.get("login", {}).get("success"):
            print("✅ Login: PASSED")
        else:
            print(f"❌ Login: FAILED - {auth.get('login', {}).get('error', 'Unknown error')}")
        
        if auth.get("me", {}).get("success"):
            print("✅ Me Endpoint: PASSED")
        else:
            print(f"❌ Me Endpoint: FAILED")
        
        # Personas
        persons = results["persons"]
        if isinstance(persons, dict):
            if persons.get("list_persons", {}).get("success"):
                print("✅ List Persons: PASSED")
            else:
                print("❌ List Persons: FAILED")
            
            if persons.get("create_person", {}).get("success"):
                print("✅ Create Person: PASSED")
            else:
                print("❌ Create Person: FAILED")
        
        # Auditoría
        audit = results["audit"]
        if isinstance(audit, dict):
            if audit.get("list_audit_logs", {}).get("success"):
                print("✅ List Audit Logs: PASSED")
            else:
                print("❌ List Audit Logs: FAILED")
        
        print()
        print("=" * 60)


if __name__ == "__main__":
    tester = APITester()
    tester.run_full_test()
