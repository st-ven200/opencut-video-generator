#!/usr/bin/env python3
import os
import sys
import argparse
from src.tts import generate_voiceover
from src.scene_builder import build_scene1, build_scene2, build_scene3, build_scene4, build_scene5
from src.video_renderer import render_final_video
from src.uploader import upload_to_uguu

DEFAULT_SCRIPT = (
    "大家好，今天为大家带来开源版剪映 OpenCut 与系统底座的深度解析，重点拆解 Kafka 为什么这么快以及 RocketMQ 哪里不如 Kafka。"
    "在现代高并发分布式系统架构中，消息队列的吞吐量直接决定了整个系统的性能上限与响应延迟。"
    "传统数据传输需要经过 4 次上下文切换与 4 次内存数据拷贝，导致 CPU 资源严重浪费。"
    "而 Linux 的零拷贝技术，例如 mmap 内存映射，将内核缓冲区映射到虚拟内存，省去了用户态拷贝；"
    "更高阶的 sendfile 系统调用配合 DMA 散射聚集机制，更是实现了真正的 CPU 零内存拷贝。"
    "Kafka 拥有四大极速底座：sendfile 零拷贝、Linux PageCache 磁盘页缓存、顺序写磁盘追加模式以及批量消息压缩传输。"
    "在选型方面，Kafka 每个 Partition 独立文件存储，适合海量日志与流处理；而 RocketMQ 单 CommitLog 共享存储，天然支持上万级 Topic 高并发与金融级事务消息。"
)

def main():
    parser = argparse.ArgumentParser(description="OpenCut 纯云端/本地自动化演示视频生成器")
    parser.add_argument("--text", type=str, default=DEFAULT_SCRIPT, help="旁白配音脚本内容")
    parser.add_argument("--output", type=str, default="output/opencut_kafka_zerocopy.mp4", help="输出视频路径")
    parser.add_argument("--temp-dir", type=str, default="temp_build", help="临时分镜与音频缓存目录")
    parser.add_argument("--upload", action="store_true", help="视频生成后自动上传至 Uguu 获取公网在线预览链接")
    args = parser.parse_args()

    os.makedirs(args.temp_dir, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    print(">>> [1/4] 正在合成云端旁白语音 (Edge-TTS 晓伊女声)...")
    audio_path = os.path.join(args.temp_dir, "narration.mp3")
    generate_voiceover(args.text, audio_path)

    print(">>> [2/4] 正在渲染 5 大 Kafka 零拷贝与架构对比高保真 1080P 分镜画布...")
    s1_path = os.path.join(args.temp_dir, "scene1.png")
    s2_path = os.path.join(args.temp_dir, "scene2.png")
    s3_path = os.path.join(args.temp_dir, "scene3.png")
    s4_path = os.path.join(args.temp_dir, "scene4.png")
    s5_path = os.path.join(args.temp_dir, "scene5.png")
    
    build_scene1(s1_path)
    build_scene2(s2_path)
    build_scene3(s3_path)
    build_scene4(s4_path)
    build_scene5(s5_path)

    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_large.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

    print(">>> [3/4] 正在调度 FFmpeg 滤镜图合成 5 大场景多轨道视频 (含 BGM、SFX 转场音效与卡点)...")
    render_final_video(s1_path, logo_path, s2_path, s3_path, s4_path, s5_path, audio_path, args.output)

    print(f"\n🎉 视频生成完成！输出路径: {args.output}")

    if args.upload:
        print("\n>>> [4/4] 正在上传视频至 Uguu 公网平台获取预览链接...")
        upload_to_uguu(args.output)

if __name__ == "__main__":
    main()
