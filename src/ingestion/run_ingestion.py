"""
Script para execução do processo de ingestão e vetorização da documentação PHP.
"""
import os
from src.config import Config
from src.ingestion.scraper import PHPLocalExtractor
from src.ingestion.vector_store import VectorStoreManager

def main():
    """
    Função principal que coordena o processo de ingestão local e vetorização.
    """
    try:
        Config.validate()
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        return

    local_file = Config.PHP_MANUAL_LOCAL_PATH
    persist_db = Config.CHROMA_DB_PATH

    print(f"Iniciando ingestão da documentação local: {local_file}")

    if not os.path.exists(local_file):
        print(f"Erro: Arquivo local não encontrado em {local_file}")
        return

    extractor = PHPLocalExtractor(local_file)
    vector_manager = VectorStoreManager(persist_db)

    # 1. Extrair conteúdo do arquivo consolidado
    print("Extraindo conteúdo do arquivo .html.gz...")
    raw_contents = extractor.get_content()

    # 2. Adicionar ao banco vetorial
    if raw_contents:
        print(f"Vetorizando documento consolidado ({len(raw_contents[0]['text'])} caracteres)...")
        # O VectorStoreManager fará o split automático em chunks
        vector_manager.add_content(raw_contents)
        print("Ingestão local concluída com sucesso!")
    else:
        print("Nenhum conteúdo extraído do arquivo local.")

if __name__ == "__main__":
    main()
