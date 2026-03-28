"""
Módulo de configuração centralizada para a aplicação.
Este módulo gerencia o carregamento de variáveis de ambiente e validações iniciais.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuração centralizada da aplicação com validação de variáveis de ambiente.
    """
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "data/chroma_db")
    PHP_MANUAL_LOCAL_PATH = os.getenv("PHP_MANUAL_LOCAL_PATH")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/chat_history.db")

    @classmethod
    def validate(cls):
        """
        Valida se as variáveis de ambiente obrigatórias estão configuradas.
        """
        missing = []
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        if not cls.PHP_MANUAL_LOCAL_PATH:
            missing.append("PHP_MANUAL_LOCAL_PATH")

        if missing:
            raise ValueError(
                f"Variáveis de ambiente obrigatórias ausentes: {', '.join(missing)}"
            )

    @classmethod
    def validate_webhook(cls):
        """
        Valida variáveis necessárias especificamente para o Webhook.
        """
        if not cls.TWILIO_AUTH_TOKEN:
            print(
                "AVISO: TWILIO_AUTH_TOKEN não configurado. "
                "A validação de assinatura do Twilio será desativada."
            )
            return False
        return True
