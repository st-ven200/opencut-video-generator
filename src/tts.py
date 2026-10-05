import asyncio
import edge_tts
import os

DEFAULT_VOICE = "zh-CN-XiaoyiNeural" # 晓伊 - 甜美轻快女声

async def generate_speech_async(text: str, output_path: str, voice: str = DEFAULT_VOICE, rate: str = "+20%", pitch: str = "+3Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)

def generate_voiceover(text: str, output_path: str, voice: str = DEFAULT_VOICE, rate: str = "+20%", pitch: str = "+3Hz"):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    asyncio.run(generate_speech_async(text, output_path, voice, rate, pitch))
    return output_path
