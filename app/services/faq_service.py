from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.faq import FAQ
from app.models.unanswered import UnansweredQuestion
from app.schemas.faq import FAQCreate, FAQUpdate
from app.services.embedding_service import EmbeddingService
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Modelo local de chat
llm = OllamaLLM(
    model="llama3.2",
    base_url="http://host.docker.internal:11434"
)

# Limiar de similaridade: distâncias L2 acima desse valor = resposta desconhecida
SIMILARITY_THRESHOLD = 1.2


class FAQService:

    @staticmethod
    async def create_faq(db: AsyncSession, faq_in: FAQCreate) -> FAQ:
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
    async def get_all(db: AsyncSession) -> list[FAQ]:
        """Retorna todos os FAQs ordenados por data de criação."""
        result = await db.execute(select(FAQ).order_by(FAQ.created_at.desc()))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, faq_id: str) -> FAQ:
        result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
        faq = result.scalar_one_or_none()
        if not faq:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAQ não encontrado")
        return faq

    @staticmethod
    async def update_faq(db: AsyncSession, faq_id: str, faq_in: FAQUpdate) -> FAQ:
        faq = await FAQService.get_by_id(db, faq_id)

        update_data = faq_in.model_dump(exclude_unset=True)

        # Se a pergunta mudou, recalcula o embedding
        if "question" in update_data:
            update_data["embedding"] = await EmbeddingService.get_embedding(update_data["question"])

        for field, value in update_data.items():
            setattr(faq, field, value)

        await db.commit()
        await db.refresh(faq)
        return faq

    @staticmethod
    async def delete_faq(db: AsyncSession, faq_id: str) -> None:
        faq = await FAQService.get_by_id(db, faq_id)
        await db.delete(faq)
        await db.commit()

    @staticmethod
    async def ask_question(db: AsyncSession, question: str) -> dict:
        """
        Fluxo RAG completo:
        1. Gera embedding da pergunta
        2. Busca FAQs similares via L2 distance
        3. Verifica se a similaridade é boa o suficiente
        4. Gera resposta com IA local usando o contexto
        5. Se não encontrar contexto relevante, salva como pergunta sem resposta
        """
        query_embedding = await EmbeddingService.get_embedding(question)

        # Busca os 3 FAQs mais similares
        result = await db.execute(
            select(FAQ).order_by(FAQ.embedding.l2_distance(query_embedding)).limit(3)
        )
        context_faqs = result.scalars().all()

        # Se não há FAQs no banco ou a similaridade é ruim, salva como não respondida
        if not context_faqs:
            await FAQService._save_unanswered(db, question, query_embedding)
            return {
                "answer": "Não encontrei informações sobre isso. Sua pergunta foi registrada para análise.",
                "source": "unanswered"
            }

        context_text = "\n".join([f"P: {f.question}\nR: {f.answer}" for f in context_faqs])

        template = """Você é o assistente inteligente do Totem Universitário EchoMind.
Use APENAS as informações abaixo para responder de forma clara e objetiva.
Se a resposta não estiver no contexto, diga que não tem essa informação e oriente o aluno a procurar a secretaria.
NÃO invente informações.

Contexto disponível:
{context}

Pergunta do aluno: {question}

Resposta:"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm

        answer = await chain.ainvoke({"question": question, "context": context_text})

        return {"answer": answer, "source": "faq"}

    @staticmethod
    async def _save_unanswered(db: AsyncSession, question: str, embedding: list) -> None:
        """Salva perguntas sem resposta para análise posterior pelo admin."""
        unanswered = UnansweredQuestion(question=question, embedding=embedding)
        db.add(unanswered)
        await db.commit()
