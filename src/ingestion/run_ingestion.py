"""
Script para execução do processo de ingestão e vetorização da documentação PHP.
"""
import os
from dotenv import load_dotenv
from src.ingestion.scraper import PHPScraper
from src.ingestion.vector_store import VectorStoreManager

load_dotenv()

def main():
    """
    Função principal que coordena o processo de scraping e vetorização.
    """
    base_url = os.getenv("PHP_MANUAL_URL")
    persist_db = os.getenv("CHROMA_DB_PATH")

    print(f"Iniciando ingestão da documentação: {base_url}")
    scraper = PHPScraper(base_url)
    vector_manager = VectorStoreManager(persist_db)

    # 1. Obter links principais
    print("Extraindo links...")
    links = scraper.get_links()
    # Para teste/demo, vamos limitar a 10 links
    links_to_process = links[:10]
    print(f"Total de links encontrados: {len(links)}.")
    print(f"Processando os primeiros {len(links_to_process)}.")

    # 2. Extrair conteúdo
    raw_contents = []
    for link in links_to_process:
        print(f"Lendo: {link}")
        content = scraper.get_content(link)
        if content:
            raw_contents.append(content)

    # 3. Adicionar ao banco vetorial
    if raw_contents:
        print(f"Vetorizando {len(raw_contents)} documentos...")
        vector_manager.add_content(raw_contents)
        print("Ingestão concluída com sucesso!")
    else:
        print("Nenhum conteúdo extraído.")

if __name__ == "__main__":
    main()
