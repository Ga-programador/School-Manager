import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_login():
    response = client.get("/login")
    assert response.status_code == 200

def test_read_dashboard():
    response = client.get("/dashboard")
    assert response.status_code == 200

def test_dashboard_metricas_autorizado():
    # Testa acesso com perfil de admin
    response = client.get("/dashboard/metricas", headers={"x-user-role": "admin"})
    assert response.status_code == 200

def test_dashboard_metricas_negado():
    # Testa bloqueio de acesso para perfil de aluno
    response = client.get("/dashboard/metricas", headers={"x-user-role": "aluno"})
    assert response.status_code == 403