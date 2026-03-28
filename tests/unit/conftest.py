"""
Configurações e fixtures globais para os testes unitários.
"""
import pytest
from src.ingestion.scraper import PHPScraper

@pytest.fixture
def php_scraper():
    """Retorna uma instância básica do PHPScraper para testes."""
    return PHPScraper("https://www.php.net/manual/pt_BR/index.php")
