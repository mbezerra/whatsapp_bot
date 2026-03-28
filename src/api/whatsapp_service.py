"""
Módulo para integração com a API do WhatsApp via Twilio.
"""
from twilio.rest import Client

class WhatsAppService:
    """
    Serviço responsável pelo envio de mensagens via Twilio WhatsApp API.
    """
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        """
        Inicializa o cliente Twilio com as credenciais da conta.
        """
        self.client = Client(account_sid, auth_token)
        self.from_number = f"whatsapp:{from_number}"

    def send_message(self, to: str, body: str):
        """
        Envia uma mensagem de texto para um número específico do WhatsApp.
        """
        message = self.client.messages.create(
            from_=self.from_number,
            body=body,
            to=f"whatsapp:{to}"
        )
        return message.sid
