"""
Módulo responsável pela extração de dados (scraping) da documentação oficial do PHP.
"""
import gzip
from typing import List, Dict
from bs4 import BeautifulSoup

class PHPLocalExtractor:
    """
    Classe responsável por extrair dados da documentação PHP a partir de um arquivo local .html.gz.
    """
    def __init__(self, file_path: str):
        """
        Inicializa o extrator com o caminho do arquivo comprimido.
        """
        self.file_path = file_path

    def get_content(self) -> List[Dict[str, str]]:
        """
        Lê o arquivo .gz e extrai o conteúdo de texto formatado.
        """
        try:
            with gzip.open(self.file_path, 'rt', encoding='utf-8') as f:
                html_content = f.read()
        except (OSError, EOFError) as e:
            print(f"Erro ao ler arquivo local (.gz): {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao processar arquivo: {e}")
            raise

        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove scripts e estilos
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # O manual consolidado pode ter uma estrutura diferente.
        # Vamos tentar pegar o body ou seções principais se houver.
        content_div = soup.find(id='layout-content') or soup.find('body')
        if not content_div:
            return []

        # Como é um arquivo único consolidado, vamos retornar uma lista com um item.
        # O VectorStoreManager se encarregará de fazer o chunking (quebra em pedaços).
        return [{
            "url": f"local://{self.file_path}",
            "title": soup.title.string if soup.title else "Manual PHP Offline",
            "text": content_div.get_text(separator=' ', strip=True)
        }]
