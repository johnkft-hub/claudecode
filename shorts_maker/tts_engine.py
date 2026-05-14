import asyncio
import os

from config import TTS_ENGINE, TTS_VOICE_KO, TTS_SPEED


async def _edge_tts_async(text: str, output_path: str):
    import edge_tts
    communicate = edge_tts.Communicate(text, TTS_VOICE_KO, rate=TTS_SPEED)
    await communicate.save(output_path)


def generate_tts(text: str, output_path: str, lang: str = "ko") -> str:
    """텍스트를 음성 파일(.mp3)로 변환 후 경로 반환."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if TTS_ENGINE == "edge-tts":
        asyncio.run(_edge_tts_async(text, output_path))
    else:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)

    return output_path
