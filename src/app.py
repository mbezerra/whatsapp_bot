"""
Aplicação Flask que atua como Webhook para integração com a API do WhatsApp via Twilio.
"""
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from src.ai.rag_service import RAGService
from src.ingestion.vector_store import VectorStoreManager
from src.models.chat_history import ChatHistoryDB

load_dotenv()

app = Flask(__name__)

# Configuração global
vector_store_manager = VectorStoreManager(os.getenv("CHROMA_DB_PATH"))
chat_history_db = ChatHistoryDB()
rag_service = RAGService(vector_store_manager, chat_history_db)

@app.route("/", methods=['GET'])
def index():
    """
    Página inicial informativa sobre o bot.
    """
    return {
        "status": "online",
        "service": "WhatsApp PHP Documentation Bot",
        "endpoint": "/webhook (POST only)"
    }, 200

@app.route("/@vite/client", methods=['GET'])
def vite_client_dummy():
    """
    Rota dummy para evitar logs de erro 404 de ferramentas de desenvolvimento (como Vite).
    """
    return "", 204

@app.route("/webhook", methods=['POST'])
def webhook():
    """
    Endpoint de Webhook que recebe mensagens do WhatsApp via Twilio,
    processa através do serviço RAG e retorna a resposta formatada em TwiML.
    """
    # Extrai a mensagem e o remetente
    incoming_msg = request.values.get('Body', '').strip()
    sender_number = request.values.get('From', '')

    # Processa via IA usando o número do remetente como ID de sessão
    response_text = rag_service.get_response(sender_number, incoming_msg)

    # Prepara resposta Twilio
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_text)

    return str(resp)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
