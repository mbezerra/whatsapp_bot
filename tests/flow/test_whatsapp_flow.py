"""
Testes de fluxo de ponta a ponta para a integração com WhatsApp.
"""
from unittest.mock import patch

def test_webhook_flow(test_client):
    """
    Testa o fluxo completo do webhook, simulando uma mensagem do Twilio.
    """
    # Simulando dados que o Twilio envia via POST
    payload = {
        'Body': 'Como usar array_map no PHP?',
        'From': 'whatsapp:+5511999999999'
    }

    # Mockando a resposta da IA para não gastar tokens ou depender de chave de API
    with patch('src.ai.rag_service.RAGService.get_response') as mock_rag:
        mock_rag.return_value = (
            "A função array_map() aplica uma callback aos elementos de um array."
        )

        response = test_client.post('/webhook', data=payload)

        assert response.status_code == 200
        assert b"array_map" in response.data
        assert b"<Response>" in response.data
        assert b"<Message>" in response.data
        mock_rag.assert_called_once_with('whatsapp:+5511999999999', 'Como usar array_map no PHP?')
