# OpenCut 自动化视频生成器 - 全量研究成果与技术工作流报告

> 本文档汇总记录了项目在 B 站视频解密提取、防风控 Cookie 接管、关键帧视觉拆解、神经语音配音管线、多轨道 BGM/SFX 混音及 OpenCut 纯云端无头渲染引擎的全量研究成果与实现过程。

---

## 目录
1. [B 站视频提取与反风控 Cookie 接管技术研究](#1-b-站视频提取与反风控-cookie-接管技术研究)
2. [视频内容与关键帧视觉设计剖析](#2-视频内容与关键帧视觉设计剖析)
3. [配音与多轨道 BGM / SFX 音效管线](#3-配音与多轨道-bgm--sfx-音效管线)
4. [OpenCut 纯云端无头渲染引擎架构](#4-opencut-纯云端无头渲染引擎架构)
5. [快速上手与 CLI 指令指南](#5-快速上手与-cli-指令指南)

---

## 1. B 站视频提取与反风控 Cookie 接管技术研究

### 1.1 痛点与风控根因
在对 B 站视频（如 `BV1Zy411e7qY`）进行纯服务器端提取时，未认证的 `yt-dlp` 或 `curl` 请求会触发 B 站安全风控策略，返回 `HTTP 412 Precondition Failed` 错误页面，阻止无头爬虫访问高码率音视频流与 API 数据。

### 1.2 `blueprint-mcp` 浏览器会话接管与 Cookie 提取
利用 `blueprint-mcp` 协议控制宿主机 Chrome 浏览器实例：
1. **浏览器连接与标签页挂载**：通过 `browser_connections` 选中宿主机浏览器，并调用 `browser_tabs` 附加到已登录 B 站账号的活跃 Tab 页面。
2. **DOM 状态对象评估**：调用 `browser_evaluate` 在网页 JS 上下文中求值 `window.__INITIAL_STATE__.videoData`，直接获取完整标题、章节打点（`chapters`）及官方 CC 字幕 JSON。
3. **Cookie 凭据提取与流解密**：调用 `browser_get_cookies` 提取 `SESSDATA`、`bili_jct`、`DedeUserID` 与 `buvid3` 凭据，导出为 Netscape Cookie 文件，实现 **100% 绕过 412 风控**，解密出 1080P 超高清视频轨（AV1/H.264）与双声道 AAC 高码率音频轨（`30280`）。

---

## 2. 视频内容与关键帧视觉设计剖析

### 2.1 案例研究视频拆解 (`BV1Zy411e7qY`：《Kafka 为什么这么快》)
对原视频 5 分 18 秒的内容进行了 6 大章节深度拆解：
- **`00:00 - 00:38`**：开篇 Hook 引言与高并发吞吐量痛点。
- **`00:38 - 01:48`**：传统 I/O 路径分析（4 次上下文切换 + 4 次内存数据拷贝）。
- **`01:48 - 02:42`**：`mmap` 内存映射（虚拟内存直接映射内核缓冲区，省去用户态拷贝）。
- **`02:42 - 03:17`**：`sendfile` 零拷贝（Linux 2.4+ DMA 散射聚集，实现 0 次 CPU 拷贝）。
- **`03:17 - 04:43`**：Kafka 4 大极速底座（sendfile + PageCache + 顺序写磁盘 + 批量压缩）。
- **`04:43 - 05:18`**：Kafka 单 Partition 文件 vs RocketMQ 单 CommitLog 多 Topic 架构抉择。

### 2.2 视觉与创作手法分析
- **配色系统**：选用 Stripe / Linear 风格深黑石墨色（`#0d0e11`），功能模块采用高饱和对比色区分（用户态内存-蓝色，内核态/硬件-绿色与红色，播放红针-红色）。
- **卡片化与手绘 IP**：将复杂的 Linux 内核与网卡模块卡片化，降低认知负荷。
- **动效卡点**：配音语速保持在 240-260 字/分钟，关键节点伴随 Pop-in 弹出音效与视线高亮。

---

## 3. 配音与多轨道 BGM / SFX 音效管线

### 3.1 神经语音配音合成 (Edge-TTS)
支持云端毫秒级生成自然流畅的神经语音，并可调节语速与音调：
- **经典搞笑男声**：`zh-CN-YunxiNeural`（`rate="+25%"`, `pitch="+5Hz"`）。
- **甜美轻快女声**：`zh-CN-XiaoyiNeural` (晓伊，`rate="+20%"`, `pitch="+3Hz"`）。
- **知性活泼女声**：`zh-CN-XiaoxiaoNeural` (晓晓)。

### 3.2 多轨道 BGM & SFX 音效合流
- **代码生成音效（`src/audio_effects.py`）**：
  - `Whoosh` (嗖/风声转场)：分镜切入卡点。
  - `Pop` (弹出/喀哒音效)：卡片/标题出现卡点。
  - `Ding` (清脆提示音)：重点要素强调卡点。
  - `Ambient BGM`：低音量（`-20dB`）双声道科技和弦和声衬底。
- **FFmpeg 复合混音 (`src/video_renderer.py`)**：
  使用 `adelay` 与 `amix` 滤镜将主旁白、BGM 与 3 轨 SFX 转场音效合流为标准的 192k AAC 声音轨道。

---

## 4. OpenCut 纯云端无头渲染引擎架构

```tree
opencut-video-generator/
├── assets/                  # 官方矢量 Logo
├── src/
│   ├── __init__.py
│   ├── config.py            # 分辨率(1080P/25FPS)、色盘与场景卡点配置
│   ├── tts.py               # Edge-TTS 神经语音合成模块
│   ├── audio_effects.py     # SFX 转场音效与 Ambient BGM 生成模块
│   ├── scene_builder.py     # 4 大高保真分镜画布绘制 (Pillow)
│   ├── video_renderer.py    # FFmpeg 多轨道复合滤镜渲染引擎
│   └── uploader.py          # Uguu 公网临时托管与在线预览上传模块
├── generate.py              # CLI 命令行一键生成与上传入口
├── requirements.txt         # 核心依赖 (edge-tts, Pillow, requests)
├── RESEARCH_AND_WORKFLOW.md # 本工程研究成果与工作流报告
└── README.md                # 项目快速开始指南
```

---

## 5. 快速上手与 CLI 指令指南

### 5.1 安装依赖
```bash
pip install -r requirements.txt
```

### 5.2 命令行生成与公网预览
```bash
# 1. 默认一键生成并自动上传公网获取预览 URL
python3 generate.py --upload

# 2. 自定义配音文本与声音类型
python3 generate.py \
  --text "大家好，这是自定义配音的技术视频！" \
  --output "output/my_demo.mp4" \
  --upload
```
