# WhatsApp AI Bot - PHP Documentation Specialist

Este projeto consiste em um assistente de IA para WhatsApp focado em responder dúvidas sobre a documentação oficial do PHP (https://www.php.net/manual/pt_BR/index.php).

## 🚀 Fases de Desenvolvimento

### Fase 1: Base de Conhecimento e RAG Foundation (Concluída ✅)
- **Meta:** Extração, processamento e vetorização da documentação do PHP.
- **Entregáveis:** 
    - [scraper.py](file:///home/mbezerra/Works/whatsapp_bot/src/ingestion/scraper.py): Módulo de scraping.
    - [vector_store.py](file:///home/mbezerra/Works/whatsapp_bot/src/ingestion/vector_store.py): Integração com ChromaDB.
- **Testes:** [test_scraper.py](file:///home/mbezerra/Works/whatsapp_bot/tests/unit/test_scraper.py).

### Fase 2: Orquestração de IA (Concluída ✅)
- **Meta:** Implementação do pipeline RAG.
- **Entregáveis:**
    - [rag_service.py](file:///home/mbezerra/Works/whatsapp_bot/src/ai/rag_service.py): Serviço de IA com LangChain.
- **Testes:** [test_rag_service.py](file:///home/mbezerra/Works/whatsapp_bot/tests/unit/test_rag_service.py).

### Fase 3: Integração com WhatsApp (Concluída ✅)
- **Meta:** Conexão com API do WhatsApp via Twilio.
- **Entregáveis:**
    - [whatsapp_service.py](file:///home/mbezerra/Works/whatsapp_bot/src/api/whatsapp_service.py): Cliente Twilio.
    - [app.py](file:///home/mbezerra/Works/whatsapp_bot/src/app.py): Webhook Flask.
- **Testes:** [test_whatsapp_flow.py](file:///home/mbezerra/Works/whatsapp_bot/tests/flow/test_whatsapp_flow.py).

### Fase 4: Gestão de Sessão e Memória (Concluída ✅)
- **Meta:** Persistência de contexto para conversas contínuas.
- **Entregáveis:**
    - [chat_history.py](file:///home/mbezerra/Works/whatsapp_bot/src/models/chat_history.py): Banco de dados SQLite para histórico.
    - Atualização no [rag_service.py](file:///home/mbezerra/Works/whatsapp_bot/src/ai/rag_service.py) para usar histórico.
- **Testes:** [test_whatsapp_flow.py](file:///home/mbezerra/Works/whatsapp_bot/tests/flow/test_whatsapp_flow.py) atualizado para validar fluxo com ID de sessão.

## 🛠️ Como Executar

### Pré-requisitos
- Python 3.10+
- Chave de API da OpenAI (configurar no `.env`)

### Instalação
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Executar Testes
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest tests/
```

### Iniciar o Bot
```bash
python src/app.py
```

## 🛠️ Stack Principal
- **Linguagem:** Python 3.10+
- **IA:** LangChain / LlamaIndex, OpenAI API (ou similar)
- **Vetores:** ChromaDB
- **WhatsApp:** Twilio API / Flask ou FastAPI para o Webhook
- **Testes:** Pytest

## 🧪 Estratégia de Testes
- **Unitários:** Testar funções isoladas (ex: formatação de texto, extração de links).
- **Fluxo (E2E):** Simular o trajeto completo da mensagem do usuário até a resposta final.
- **Integração:** Validar a comunicação entre módulos (IA <-> Banco Vetorial, Webhook <-> IA).
