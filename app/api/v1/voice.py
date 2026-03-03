import time, os
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.ai_service import AIService
from app.services.embedding_service import EmbeddingService
from app.utils.vector_search import VectorSearch
from app.models.interaction import Interaction

router = APIRouter(prefix="/voice-query", tags=["AI Agent"])

@router.post("/")
async def voice_query(audio: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    start_ts = time.time()
    
    # Save temp
    temp_name = f"temp_{audio.filename}"
    with open(temp_name, "wb") as f:
        f.write(await audio.read())
    
    # Process
    user_text = await AIService.transcribe_audio(temp_name)
    embedding = await EmbeddingService.get_embedding(user_text)
    context = await VectorSearch.find_similar_context(db, embedding)
    
    ai_text = await AIService.generate_text_response(user_text, context)
    audio_path = await AIService.text_to_speech(ai_text)
    
    duration = time.time() - start_ts
    
    # Log
    new_inter = Interaction(question=user_text, answer=ai_text, response_time=duration)
    db.add(new_inter)
    await db.commit()
    
    os.remove(temp_name)
    
    return {
        "text_response": ai_text,
        "audio_url": audio_path,
        "response_time": duration
    }
