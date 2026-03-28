"""
Aplicação Flask que atua como Webhook para integração com a API do WhatsApp via Twilio.
"""
import logging
import sqlite3
import sys
from functools import wraps
from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from src.config import Config
from src.ai.rag_service import RAGService
from src.ingestion.vector_store import VectorStoreManager
from src.models.chat_history import ChatHistoryDB

# Validação inicial de configuração
try:
    Config.validate()
except ValueError as e:
    print(f"Erro de configuração crítica: {e}")
    sys.exit(1)

app = Flask(__name__)

# Configuração global
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

vector_store_manager = VectorStoreManager(Config.CHROMA_DB_PATH)
chat_history_db = ChatHistoryDB(Config.DATABASE_PATH)
rag_service = RAGService(vector_store_manager, chat_history_db)

def validate_twilio_request(f):
    """
    Decorador para validar se a requisição provém do Twilio.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not Config.validate_webhook():
            return f(*args, **kwargs)

        validator = RequestValidator(Config.TWILIO_AUTH_TOKEN)
        signature = request.headers.get('X-Twilio-Signature', '')

        # O Twilio envia a URL completa incluindo protocolo e host
        url = request.url

        # Dados do formulário POST
        data = request.form.to_dict()

        if not validator.validate(url, data, signature):
            print(f"Falha na validação de assinatura Twilio para URL: {url}")
            abort(403)

        return f(*args, **kwargs)
    return decorated_function

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
@validate_twilio_request
def webhook():
    """
    Endpoint de Webhook que recebe mensagens do WhatsApp via Twilio,
    processa através do serviço RAG e retorna a resposta formatada em TwiML.
    """
    resp = MessagingResponse()

    try:
        # Extrai a mensagem e o remetente
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '')

        if not incoming_msg:
            return str(resp)

        # Processa via IA usando o número do remetente como ID de sessão
        response_text = rag_service.get_response(sender_number, incoming_msg)

        # Prepara resposta Twilio
        msg = resp.message()
        msg.body(response_text)

    except (sqlite3.Error, ValueError, RuntimeError) as e:
        # Erros esperados de infraestrutura ou validação
        logger.error("Erro processável no webhook: %s", e)
        error_msg = resp.message()
        error_msg.body("Houve um problema temporário. Por favor, tente novamente em instantes.")

    except Exception as e:  # pylint: disable=broad-except
        # Fallback de segurança para garantir que o Twilio receba uma resposta válida (TwiML)
        logger.exception("Erro inesperado de nível superior no webhook: %s", str(e))
        error_msg = resp.message()
        error_msg.body("Desculpe, ocorreu um erro técnico ao processar sua solicitação.")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5001, debug=Config.FLASK_DEBUG)
