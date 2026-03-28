"""
Módulo responsável pela extração de dados (scraping) da documentação oficial do PHP.
"""
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

class PHPScraper:
    """
    Classe responsável por realizar o scraping da documentação do PHP.
    """
    def __init__(self, base_url: str):
        """
        Inicializa o scraper com a URL base da documentação.
        """
        self.base_url = base_url

    def get_links(self) -> List[str]:
        """Extrai os links principais do manual."""
        response = requests.get(self.base_url, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        # Exemplo simplificado: pegando links de seções principais
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('.php') and not href.startswith('http'):
                full_url = self.base_url.rsplit('/', 1)[0] + '/' + href
                if full_url not in links:
                    links.append(full_url)
        return links

    def get_content(self, url: str) -> Dict[str, str]:
        """Extrai o conteúdo de uma página do manual."""
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove scripts e estilos
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        content_div = soup.find('div', id='layout-content')
        if not content_div:
            return {}

        return {
            "url": url,
            "title": soup.title.string if soup.title else "PHP Documentation",
            "text": content_div.get_text(separator=' ', strip=True)
        }
