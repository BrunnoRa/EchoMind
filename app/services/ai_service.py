import time
from openai import AsyncOpenAI
from app.core.config import settings
import httpx

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class AIService:
    @staticmethod
    async def transcribe_audio(file_path: str) -> str:
        with open(file_path, "rb") as audio:
            transcript = await client.audio.transcriptions.create(
                model="whisper-1", file=audio
            )
        return transcript.text

    @staticmethod
    async def generate_text_response(prompt: str, context: str) -> str:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": f"Você é um assistente de totem universitário. Use este contexto: {context}"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    @staticmethod
    async def text_to_speech(text: str) -> str:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.ELEVENLABS_VOICE_ID}"
        headers = {"xi-api-key": settings.ELEVENLABS_API_KEY}
        data = {"text": text, "model_id": "eleven_multilingual_v2"}
        
        async with httpx.AsyncClient() as ac:
            resp = await ac.post(url, json=data, headers=headers)
            if resp.status_code == 200:
                path = f"static/audio_{int(time.time())}.mp3"
                with open(path, "wb") as f:
                    f.write(resp.content)
                return path
        return ""