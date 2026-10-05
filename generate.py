#!/usr/bin/env python3
import os
import sys
import argparse
from src.tts import generate_voiceover
from src.scene_builder import build_scene1, build_scene2, build_scene3, build_scene4
from src.video_renderer import render_final_video
from src.uploader import upload_to_uguu

DEFAULT_SCRIPT = (
    "大家好，今天为大家深度解析 OpenCut 开源自动化视频生成器的核心架构与实战使用方法。"
    "首先，在环境准备阶段，只需运行 pip install -r requirements.txt 快速安装 Edge-TTS 和 Pillow 核心依赖。"
    "接着，通过命令行运行 generate.py，传入 --text 指定自定义旁白文案，并通过 --output 参数指定导出视频路径。"
    "系统会自动调用 Edge-TTS 合成高质神经语音，配合 Pillow 绘制 1080P 高保真暗黑风格多场景分镜。"
    "最后，调度 FFmpeg 复合滤镜图，实现包含视频轨、波形轨、字幕轨与动态红线指针的多轨道视频平滑导出。"
)

def main():
    parser = argparse.ArgumentParser(description="OpenCut 纯云端/本地自动化演示视频生成器")
    parser.add_argument("--text", type=str, default=DEFAULT_SCRIPT, help="旁白配音脚本内容")
    parser.add_argument("--output", type=str, default="output/opencut_tutorial.mp4", help="输出视频路径")
    parser.add_argument("--temp-dir", type=str, default="temp_build", help="临时分镜与音频缓存目录")
    parser.add_argument("--upload", action="store_true", help="视频生成后自动上传至 Uguu 获取公网在线预览链接")
    args = parser.parse_args()

    os.makedirs(args.temp_dir, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    print(">>> [1/4] 正在合成云端旁白语音 (Edge-TTS)...")
    audio_path = os.path.join(args.temp_dir, "narration.mp3")
    generate_voiceover(args.text, audio_path)

    print(">>> [2/4] 正在渲染 4 大场景高保真 1080P 分镜画布 (使用方法/CLI实战/多轨道时间轴/架构支柱)...")
    s1_path = os.path.join(args.temp_dir, "scene1.png")
    s2_path = os.path.join(args.temp_dir, "scene2.png")
    s3_path = os.path.join(args.temp_dir, "scene3.png")
    s4_path = os.path.join(args.temp_dir, "scene4.png")
    
    build_scene1(s1_path)
    build_scene2(s2_path)
    build_scene3(s3_path)
    build_scene4(s4_path)

    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_large.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

    print(">>> [3/4] 正在调度 FFmpeg 滤镜图合成多场景动态视频 (含时间轴动态指针与场景切换)...")
    render_final_video(s1_path, logo_path, s2_path, s3_path, s4_path, audio_path, args.output)

    print(f"\n🎉 视频生成完成！输出路径: {args.output}")

    if args.upload:
        print("\n>>> [4/4] 正在上传视频至 Uguu 公网平台获取预览链接...")
        upload_to_uguu(args.output)

if __name__ == "__main__":
    main()
