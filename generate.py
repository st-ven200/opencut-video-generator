#!/usr/bin/env python3
import os
import sys
import argparse
from src.tts import generate_voiceover
from src.scene_builder import build_scene1, build_scene2, build_scene3
from src.video_renderer import render_final_video

DEFAULT_SCRIPT = (
    "大家好，今天为大家带来开源版剪映 OpenCut 的核心架构与实战解析。"
    "OpenCut 专为 AI Agent 自动化视频生成深度设计，提供模块化时间轴、多轨道音视频编排与极低延迟的预览引擎。"
    "通过全链路 CI/CD 自动化流水线与 Rust 超低延迟核心，开发者可以轻松构建属于自己的自动化剪辑工作流，告别商业软件限制。"
)

def main():
    parser = argparse.ArgumentParser(description="OpenCut 纯云端/本地自动化演示视频生成器")
    parser.add_argument("--text", type=str, default=DEFAULT_SCRIPT, help="旁白配音脚本内容")
    parser.add_argument("--output", type=str, default="output/opencut_tutorial.mp4", help="输出视频路径")
    parser.add_argument("--temp-dir", type=str, default="temp_build", help="临时分镜与音频缓存目录")
    args = parser.parse_args()

    os.makedirs(args.temp_dir, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    print(">>> [1/4] 正在合成云端旁白语音 (edge-tts)...")
    audio_path = os.path.join(args.temp_dir, "narration.mp3")
    generate_voiceover(args.text, audio_path)

    print(">>> [2/4] 正在渲染多场景高保真分镜画布...")
    s1_path = os.path.join(args.temp_dir, "scene1.png")
    s2_path = os.path.join(args.temp_dir, "scene2.png")
    s3_path = os.path.join(args.temp_dir, "scene3.png")
    
    build_scene1(s1_path)
    build_scene2(s2_path)
    build_scene3(s3_path)

    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_large.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

    print(">>> [3/4] 正在调度 FFmpeg 滤镜图合成多场景动态视频 (含时间轴动态指针与场景切换)...")
    render_final_video(s1_path, logo_path, s2_path, s3_path, audio_path, args.output)

    print(f"\n🎉 视频生成完成！输出路径: {args.output}")

if __name__ == "__main__":
    main()
