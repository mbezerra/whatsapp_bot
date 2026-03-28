"""
Testes unitários para o módulo PHPLocalExtractor.
"""
import gzip
from unittest.mock import patch, mock_open

def test_get_content_returns_list(php_scraper):
    """
    Valida que o extrator lê corretamente o arquivo .gz e retorna uma lista.
    """
    html_content = "<html><title>PHP Manual</title><body><div id='layout-content'>Conteúdo PHP</div></body></html>"
    
    with patch('gzip.open', mock_open(read_data=html_content.encode('utf-8'))):
        content = php_scraper.get_content()
        assert isinstance(content, list)
        assert len(content) == 1
        assert content[0]['text'] == "Conteúdo PHP"
        assert "url" in content[0]
        assert content[0]['title'] == "PHP Manual"
