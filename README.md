# OpenCut Video Generator (开源版剪映自动化视频生成器)

> 纯云端/本地环境自动化生产高品质横屏技术演示视频系统。为 AI Agent 深度设计的端到端音视频合成管线。

---

## 🌟 核心特性

- **纯云端/无头渲染 (Headless Pipeline)**：无需物理显卡与真实显示器，依托 CPU、FFmpeg 与 Pillow 在 Linux 环境极速出片。
- **高阶美学设计 (Linear/Stripe 暗调调色)**：
  - 彻底告别大红大绿与廉价高饱和“AI 感”；
  - 采用 `#0d0e11` 石墨黑暗色多层次面板、精准边框划分与微卡片设计；
  - 全量挂载文泉驿微米黑，彻底消除中文字体豆腐块与字符乱码。
- **真实剪辑器实景多轨道仿真**：
  - 逼真的多轨道视图：视频轨、动态声波高低振幅音频轨、逐字字幕轨；
  - 动态红色播放指针 (Playhead)：时间轴匀速平滑位移，还原专业剪辑操作流程；
  - AI Agent 终端自动化代码视窗与实时监视窗口。
- **毫秒级云端语音旁白 (Edge-TTS)**：
  - 接入高质量微软神经语音（`zh-CN-YunxiNeural`），语调自然专业。
- **仓库极致轻量铁律**：
  - 严格通过 `.gitignore` 屏蔽所有视频（`*.mp4`）、长音频（`*.mp3`）与渲染切片；
  - 仓库内仅包含核心代码、矢量素材与工程配置，保持 Git 历史极速拉取。

---

## 🛠️ 目录架构

```tree
opencut-video-generator/
├── assets/                  # 官方矢量 Logo 与品牌素材 (仅存轻量级矢量图)
│   ├── logo.svg
│   ├── logo.png
│   └── logo_large.png
├── src/
│   ├── __init__.py
│   ├── config.py            # 分辨率(1080P)、帧率(25FPS)、色盘与分镜时序配置
│   ├── tts.py               # 边缘 TTS 语音合成管线
│   ├── scene_builder.py     # 多场景分镜排版 (Intro / 实景多轨 / 架构卡片)
│   └── video_renderer.py    # FFmpeg Complex Filtergraph 复合滤镜多轨合成引擎
├── generate.py              # 命令行一键生成入口
├── requirements.txt         # 核心依赖清单
├── .gitignore               # 严格的二进制音视频与临时缓存隔离规则
└── README.md                # 完整工程技术文档
```

---

## 🚀 快速开始

### 1. 安装系统依赖与 Python 库

确保环境已安装 `ffmpeg` 与中文字体：

```bash
# Ubuntu / Debian
sudo apt-get update && sudo apt-get install -y ffmpeg fonts-wqy-microhei

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 一键生成视频

直接运行默认脚本生成完整的 1080P 多分镜演示视频：

```bash
python3 generate.py
```

自定义配音台词与输出路径：

```bash
python3 generate.py \
  --text "大家好，这是自定义的一键生成技术视频！" \
  --output "output/my_custom_video.mp4"
```

---

## 📜 许可证

本项目遵循 MIT 许可证开箱即用。
