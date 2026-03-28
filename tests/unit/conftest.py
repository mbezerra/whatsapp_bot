"""
Configurações e fixtures globais para os testes unitários.
"""
import pytest
from src.ingestion.scraper import PHPLocalExtractor

@pytest.fixture
def php_scraper():
    """Retorna uma instância básica do PHPLocalExtractor para testes."""
    return PHPLocalExtractor("dummy.html.gz")
