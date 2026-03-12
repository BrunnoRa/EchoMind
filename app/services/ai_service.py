import os
import time
import asyncio
import edge_tts
from faster_whisper import WhisperModel

_whisper_model: WhisperModel | None = None


def get_whisper_model() -> WhisperModel:
    global _whisper_model
    if _whisper_model is None:
        print("🎙️  Carregando modelo Whisper (base)... (apenas na primeira vez)")
        _whisper_model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"  # otimizado para CPU
        )
        print("✅ Whisper carregado.")
    return _whisper_model


class AIService:

    @staticmethod
    async def transcribe_audio(file_path: str) -> str:
        """
        Transcreve áudio para texto usando Whisper local (faster-whisper).
        Roda em thread separada para não bloquear o event loop do FastAPI.
        """
        def _transcribe():
            model = get_whisper_model()
            segments, info = model.transcribe(
                file_path,
                language="pt",          # força português para melhor precisão
                beam_size=5,
                vad_filter=True,        # remove silêncio automaticamente
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            return " ".join(segment.text.strip() for segment in segments)

        # Executa em thread para não bloquear o async loop
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, _transcribe)
        return text.strip()

    @staticmethod
    async def text_to_speech(text: str) -> str:
        """
        Converte texto em áudio usando Edge TTS (Microsoft).
        Gratuito, sem chave de API, voz pt-BR de alta qualidade.
        Vozes disponíveis PT-BR:
          - pt-BR-FranciscaNeural  (feminina, natural)
          - pt-BR-AntonioNeural    (masculina, natural)
        """
        os.makedirs("static", exist_ok=True)
        output_path = f"static/audio_{int(time.time())}.mp3"

        communicate = edge_tts.Communicate(
            text=text,
            voice="pt-BR-FranciscaNeural"
        )
        await communicate.save(output_path)

        return output_path
