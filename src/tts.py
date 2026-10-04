import asyncio
import edge_tts
import os

DEFAULT_VOICE = "zh-CN-YunxiNeural" # 温暖富有科技感的专业男声

async def generate_speech_async(text: str, output_path: str, voice: str = DEFAULT_VOICE):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_voiceover(text: str, output_path: str, voice: str = DEFAULT_VOICE):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    asyncio.run(generate_speech_async(text, output_path, voice))
    return output_path
