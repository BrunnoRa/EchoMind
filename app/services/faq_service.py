from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.faq import FAQ
from app.services.embedding_service import EmbeddingService
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Configuração do modelo de chat local
llm = OllamaLLM(
    model="llama3.2",
    base_url="http://host.docker.internal:11434"
)

class FAQService:
    @staticmethod
    async def create_faq(db: AsyncSession, faq_in):
        # Gera o embedding localmente antes de salvar no banco
        embedding = await EmbeddingService.get_embedding(faq_in.question)
        
        new_faq = FAQ(
            question=faq_in.question,
            answer=faq_in.answer,
            category=faq_in.category,
            embedding=embedding
        )
        
        db.add(new_faq)
        await db.commit()
        await db.refresh(new_faq)
        return new_faq

    @staticmethod
    async def ask_question(db: AsyncSession, question: str):
        # 1. Gera o embedding da pergunta do usuário
        query_embedding = await EmbeddingService.get_embedding(question)
        
        # 2. Busca no banco por similaridade (RAG)
        # Nota: Assume-se que você está usando a função de distância do pgvector
        result = await db.execute(
            select(FAQ).order_by(FAQ.embedding.l2_distance(query_embedding)).limit(3)
        )
        context_faqs = result.scalars().all()
        
        # 3. Prepara o contexto para a IA
        context_text = "\n".join([f"P: {f.question} R: {f.answer}" for f in context_faqs])
        
        # 4. Prompt para a IA local
        template = """
        Você é o assistente inteligente do Totem Universitário EchoMind.
        Use as informações abaixo para responder de forma clara e prestativa.
        Se não souber a resposta, oriente o aluno a procurar a secretaria.

        Contexto:
        {context}

        Pergunta do Aluno: {question}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm
        
        return await chain.ainvoke({"question": question, "context": context_text})