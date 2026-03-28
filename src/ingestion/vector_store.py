"""Module for managing vector stores using OpenAI embeddings and Chroma vector database.

This module provides a VectorStoreManager class that simplifies the process of
creating, updating, and querying vector stores. It handles document chunking,
embedding generation, and persistence using Chroma as the vector database backend.

Key features:
- Automatic text splitting and chunking with configurable parameters
- Integration with OpenAI embeddings for semantic representation
- Persistent storage of vector embeddings
- Simple interface for adding content and creating retrievers

Example usage:
    manager = VectorStoreManager("./vector_db")
    manager.add_content([{"text": "Sample text", "url": "http://example.com", "title": "Example"}])
    retriever = manager.get_retriever()
"""

from typing import List, Dict
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class VectorStoreManager:
    """
    Gerenciador do banco de dados vetorial (ChromaDB).
    Responsável pela fragmentação de documentos, geração de embeddings e persistência.
    Utiliza modelos locais do HuggingFace para embeddings (gratuito).
    """
    def __init__(self, persist_directory: str):
        """
        Inicializa o gerenciador com o diretório de persistência e modelo de embeddings.
        """
        self.persist_directory = persist_directory
        # Usando um modelo de embeddings local e gratuito
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    def add_content(self, raw_contents: List[Dict[str, str]]):
        """
        Transforma conteúdo bruto em documentos e adiciona ao banco vetorial.
        """
        documents = []
        for item in raw_contents:
            doc = Document(
                page_content=item['text'],
                metadata={"url": item['url'], "title": item['title']}
            )
            documents.append(doc)

        split_docs = self.text_splitter.split_documents(documents)

        vector_db = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return vector_db

    def get_retriever(self):
        """
        Retorna um retriever para busca semântica no banco vetorial.
        """
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        ).as_retriever()
