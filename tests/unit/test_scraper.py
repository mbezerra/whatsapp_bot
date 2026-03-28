"""
Testes unitários para o módulo PHPScraper.
"""
from unittest.mock import patch

def test_get_links_empty_on_error(php_scraper):
    """
    Valida que o scraper retorna uma lista vazia em caso de erro HTTP.
    """
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        php_scraper.base_url = "https://example.com"
        assert php_scraper.get_links() == []

def test_get_content_returns_dict(php_scraper):
    """
    Valida que o scraper extrai corretamente o conteúdo de uma página.
    """
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><div id='layout-content'>Conteúdo PHP</div></html>"
        content = php_scraper.get_content("https://example.com/page.php")
        assert content['text'] == "Conteúdo PHP"
        assert "url" in content
