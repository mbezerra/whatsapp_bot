"""
Configurações e fixtures para os testes de fluxo.
"""
import pytest
from src.app import app

@pytest.fixture
def test_client():
    """Retorna um cliente de teste para a aplicação Flask."""
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c
