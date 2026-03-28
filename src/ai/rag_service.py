"""
Serviço de IA que implementa o pipeline RAG (Retrieval-Augmented Generation) para o bot.
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from src.ingestion.vector_store import VectorStoreManager
from src.models.chat_history import ChatHistoryDB

class RAGService:
    """
    Serviço que gerencia a lógica de Retrieval-Augmented Generation (RAG).
    Responsável por buscar contexto relevante no banco vetorial e gerar respostas
    utilizando o LLM da OpenAI, mantendo o histórico da conversa.
    """
    def __init__(self, vector_store_manager: VectorStoreManager, chat_history_db: ChatHistoryDB):
        """
        Inicializa o serviço RAG com os gerenciadores de vetores e histórico.
        """
        self.vector_store_manager = vector_store_manager
        self.chat_history_db = chat_history_db
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.template = """Você é um assistente especialista na documentação do PHP.
Use o contexto e o histórico de conversa para responder à pergunta do usuário.
Se você não souber a resposta, diga que não encontrou na documentação oficial.

Contexto:
{context}

Resposta:"""
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.template),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])

    def get_response(self, session_id: str, question: str) -> str:
        """
        Gera uma resposta para a pergunta do usuário baseada no contexto e histórico.
        """
        retriever = self.vector_store_manager.get_retriever()

        # Recuperar histórico do banco
        db_history = self.chat_history_db.get_history(session_id)
        chat_history = []
        for role, content in db_history:
            if role == "human":
                chat_history.append(HumanMessage(content=content))
            else:
                chat_history.append(AIMessage(content=content))

        def format_docs(docs):
            return "\n\n".join([d.page_content for d in docs])

        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
                "chat_history": lambda x: chat_history
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        response = rag_chain.invoke(question)

        # Salvar no banco
        self.chat_history_db.add_message(session_id, "human", question)
        self.chat_history_db.add_message(session_id, "ai", response)

        return response
