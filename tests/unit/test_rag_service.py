"""
Testes unitários para o serviço RAG (Retrieval-Augmented Generation).
"""
from unittest.mock import MagicMock, patch
from src.ai.rag_service import RAGService

@patch('src.ai.rag_service.ChatGroq')
def test_rag_service_initialization(_mock_chat):
    """
    Testa se o serviço RAG é inicializado com os parâmetros corretos.
    """
    mock_vector_manager = MagicMock()
    mock_chat_db = MagicMock()
    service = RAGService(mock_vector_manager, mock_chat_db)
    assert service.llm is not None
    assert "PHP" in service.template

@patch('src.ai.rag_service.ChatGroq')
def test_get_response_calls_llm(mock_chat):
    """
    Valida se o serviço RAG invoca corretamente o LLM e processa a resposta.
    """
    # Setup mock
    mock_llm_instance = MagicMock()
    mock_chat.return_value = mock_llm_instance
    mock_llm_instance.invoke.return_value = MagicMock(content="Resposta mockada")

    mock_vector_manager = MagicMock()
    mock_chat_db = MagicMock()
    mock_chat_db.get_history.return_value = []

    mock_retriever = MagicMock()
    mock_vector_manager.get_retriever.return_value = mock_retriever
    mock_retriever.get_relevant_documents.return_value = []

    service = RAGService(mock_vector_manager, mock_chat_db)

    mock_target = 'langchain_core.output_parsers.string.StrOutputParser.invoke'
    with patch(mock_target, return_value="Resposta mockada"):
        response = service.get_response("session123", "Como usar array_map?")
        assert response == "Resposta mockada"
