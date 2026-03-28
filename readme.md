# PHP Doc Assistant - WhatsApp AI Bot

Assistente inteligente para WhatsApp especializado na documentação oficial do PHP. Utiliza uma arquitetura RAG (Retrieval-Augmented Generation) para fornecer respostas técnicas precisas, concisas e contextualizadas diretamente do manual oficial.

## 🛠️ Arquitetura e Stack Técnica

O projeto utiliza uma stack moderna focada em performance e eficiência de custos:

- **LLM:** Groq (Llama 3.1 8B) para geração de respostas ultra-rápidas.
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`) processados localmente (CPU/GPU).
- **Vector Store:** ChromaDB para armazenamento e busca semântica de alta performance.
- **Backend:** Flask (Python 3.12+) atuando como Webhook para integração.
- **Persistência:** SQLite para gestão de histórico de conversas e memória de sessão.
- **Integração WhatsApp:** Twilio Messaging API.

## 📁 Estrutura do Projeto

- `src/ingestion/`: Módulos de extração ([scraper.py](file:///home/mbezerra/Works/whatsapp_bot/src/ingestion/scraper.py)) e vetorização ([vector_store.py](file:///home/mbezerra/Works/whatsapp_bot/src/ingestion/vector_store.py)).
- `src/ai/`: Orquestração do pipeline RAG ([rag_service.py](file:///home/mbezerra/Works/whatsapp_bot/src/ai/rag_service.py)).
- `src/models/`: Camada de dados e histórico ([chat_history.py](file:///home/mbezerra/Works/whatsapp_bot/src/models/chat_history.py)).
- `src/app.py`: Ponto de entrada da aplicação e rotas do Webhook.
- `tests/`: Suíte completa de testes unitários, de fluxo e integração.

## 🚀 Configuração e Instalação

### 1. Pré-requisitos
- Python 3.10 ou superior.
- API Key da **Groq** (obtenha gratuitamente em [console.groq.com](https://console.groq.com)).

### 2. Ambiente e Dependências
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
GROQ_API_KEY=sua_chave_aqui
CHROMA_DB_PATH=./data/chroma_db
PHP_MANUAL_URL=https://www.php.net/manual/pt_BR/index.php
```

### 4. Ingestão da Base de Conhecimento
Execute o script para popular o banco vetorial com a documentação oficial:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python src/ingestion/run_ingestion.py
```

## ⚙️ Execução e Testes

### Iniciar o Servidor
```bash
python src/app.py
```
O serviço estará disponível em `http://localhost:5001`.

### Simulação de Mensagem (Teste de Fluxo)
```bash
curl -X POST http://localhost:5001/webhook \
     -d "Body=Como funciona o array_map?" \
     -d "From=whatsapp:+5511999999999"
```

### Executar Suíte de Testes
```bash
pytest tests/
```

## 🧪 Estratégia de Qualidade
- **Testes Unitários:** Validam a lógica isolada de scraping, processamento de texto e armazenamento.
- **Testes de Fluxo:** Simulam o ciclo de vida completo de uma mensagem, desde a chegada no Webhook até a geração da resposta TwiML.
- **Gestão de Sessão:** O sistema identifica o usuário via `From` do WhatsApp e mantém o contexto da conversa utilizando SQLite.

## 📝 Notas de Implementação
- O bot roda na porta **5001** para evitar conflitos comuns com serviços de sistema.
- A rota `/@vite/client` está mapeada para evitar ruídos de logs em ambientes de desenvolvimento.
