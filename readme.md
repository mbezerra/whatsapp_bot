# PHP Doc Assistant - WhatsApp AI Bot

Assistente inteligente para WhatsApp especializado na documentação oficial do PHP. Utiliza uma arquitetura RAG (Retrieval-Augmented Generation) para fornecer respostas técnicas precisas, concisas e contextualizadas diretamente do manual oficial.

## 🛠️ Arquitetura e Stack Técnica

O projeto utiliza uma stack moderna focada em performance e eficiência de custos:

- **LLM:** Groq (Llama 3.3 70B) para geração de respostas de alta fidelidade e aderência a instruções.
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`) processados localmente (CPU/GPU).
- **Vector Store:** ChromaDB para armazenamento e busca semântica de alta performance.
- **Backend:** Flask (Python 3.12+) atuando como Webhook para integração.
- **Persistência:** SQLite para gestão de histórico de conversas e memória de sessão.
- **Configuração:** Módulo centralizado com validação rigorosa de variáveis de ambiente.
- **Segurança:** Validação de assinatura Twilio para proteção do Webhook.
- **Integração WhatsApp:** Twilio Messaging API.

## 📁 Estrutura do Projeto

- `src/ingestion/`: Módulos de extração ([scraper.py](src/ingestion/scraper.py)) e vetorização ([vector_store.py](src/ingestion/vector_store.py)).
- `src/ai/`: Orquestração do pipeline RAG ([rag_service.py](src/ai/rag_service.py)).
- `src/models/`: Camada de dados e histórico ([chat_history.py](src/models/chat_history.py)).
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
Crie um arquivo `.env` na raiz do projeto (veja `.env.sample` para referência):
```env
GROQ_API_KEY=sua_chave_aqui
CHROMA_DB_PATH=./data/chroma_db
PHP_MANUAL_LOCAL_PATH=./php_doc/php_manual_pt_BR.html.gz
TWILIO_AUTH_TOKEN=seu_auth_token_aqui
FLASK_DEBUG=True
```

### 4. Ingestão da Base de Conhecimento
Execute o script para popular o banco vetorial a partir do arquivo local consolidado:
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

### 📱 Testando com WhatsApp Real (Twilio Sandbox)
Para testar o bot com um dispositivo real, siga estes passos:

1. **Exponha seu servidor local:**
   O Twilio precisa de uma URL HTTPS pública. Use o **ngrok** para criar um túnel:
   ```bash
   # Instale o ngrok (se não tiver): pip install pyngrok ou baixe em ngrok.com
   ngrok http 5001
   ```
   Copie a URL gerada (ex: `https://abcd-123.ngrok-free.app`).

2. **Configure o Sandbox da Twilio:**
   - Acesse o [Console Twilio](https://console.twilio.com/) > Messaging > Try it out > Send a WhatsApp message.
   - Siga as instruções para ativar o Sandbox no seu celular (enviando a mensagem `join <palavra-chave>`).
   - Na aba **Sandbox Settings**, cole sua URL do ngrok no campo "When a message comes in":
     `https://abcd-123.ngrok-free.app/webhook`
   - Salve as configurações.

3. **Validação de Segurança:**
   Certifique-se de que o `TWILIO_AUTH_TOKEN` no seu `.env` é o mesmo do seu Dashboard Twilio para que a validação de assinatura funcione.

4. **Interaja:**
   Envie mensagens para o número do Sandbox no seu WhatsApp e receba as respostas da documentação PHP!

### Executar Suíte de Testes
```bash
pytest tests/
```

## 🧪 Estratégia de Qualidade
- **Testes Unitários:** Validam a lógica isolada de extração local, processamento de texto e armazenamento.
- **Testes de Fluxo:** Simulam o ciclo de vida completo de uma mensagem, desde a chegada no Webhook até a geração da resposta TwiML.
- **Validação de Webhook:** O sistema inclui validação de assinatura do Twilio para garantir que as mensagens venham de fontes confiáveis.
- **Gestão de Sessão:** O sistema identifica o usuário via `From` do WhatsApp e mantém o contexto da conversa utilizando SQLite.

## 📝 Notas de Implementação
- O bot roda na porta **5001** para evitar conflitos comuns com serviços de sistema.
- A rota `/@vite/client` está mapeada para evitar ruídos de logs em ambientes de desenvolvimento.

## 🚀 Deploy em Produção

Para ambientes de produção, siga as recomendações abaixo:

### 1. Servidor WSGI
Não utilize o servidor de desenvolvimento do Flask. Recomendamos o **Gunicorn**:
```bash
pip install gunicorn
export PYTHONPATH=$PYTHONPATH:$(pwd)
gunicorn --bind 0.0.0.0:5001 src.app:app
```

### 2. HTTPS e Webhooks
O WhatsApp (via Twilio ou Meta) exige que o endpoint do Webhook seja **HTTPS**.
- Utilize um certificado SSL válido (ex: Let's Encrypt).
- Configure um Proxy Reverso como **Nginx** ou **Apache** à frente da aplicação.

### 3. Persistência de Dados
Certifique-se de que a pasta `data/` tenha permissões de escrita para o usuário que executa a aplicação. Em ambientes de containers (Docker), monte esta pasta como um volume persistente para não perder o histórico de chat e o banco vetorial.

### 4. Variáveis de Ambiente
Em produção, prefira configurar as variáveis de ambiente diretamente no sistema ou no gerenciador de segredos do seu provedor de nuvem (AWS Secrets Manager, GCP Secret Manager, etc), em vez de utilizar o arquivo `.env`.

### 5. Ingestão de Dados
O processo de ingestão (`run_ingestion.py`) deve ser executado pelo menos uma vez no ambiente de produção para construir o banco vetorial local inicial.
