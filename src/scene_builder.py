import os
import math
from PIL import Image, ImageDraw, ImageFont
from .config import WIDTH, HEIGHT, FONT_FILE, COLORS

def get_font(size):
    try:
        return ImageFont.truetype(FONT_FILE, size)
    except Exception:
        return ImageFont.load_default()

def draw_capsule(draw, xy, text, font, text_color, bg_color, border_color=None):
    x, y, w, h = xy
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg_color, outline=border_color, width=1)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (w - tw) // 2, y + (h - th) // 2 - 2), text, font=font, fill=text_color)

def draw_waveform(draw, x, y, w, h, color):
    points_up = []
    points_down = []
    steps = 140
    mid_y = y + h // 2
    for i in range(steps):
        px = x + (i / steps) * w
        env = math.sin((i / steps) * math.pi)
        wave = math.sin(i * 0.45) * 0.6 + math.cos(i * 0.8) * 0.4
        amp = abs(wave) * env * (h * 0.42)
        points_up.append((px, mid_y - amp))
        points_down.append((px, mid_y + amp))
    points = points_up + list(reversed(points_down))
    draw.polygon(points, fill=color)

def build_scene1(output_path):
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_huge = get_font(68)
    f_sub = get_font(26)
    f_badge = get_font(18)

    draw_capsule(draw, (WIDTH // 2 - 160, 480, 320, 44), "100% 开源 · 纯云端/无头渲染", f_badge, COLORS['accent_blue'], (20, 35, 60, 255), COLORS['accent_blue'])
    
    title = "OpenCut 开源剪辑自动化生成器"
    bbox = f_huge.getbbox(title)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, 550), title, font=f_huge, fill=COLORS['text_main'])

    sub = "深挖使用方法与自动化全流程 · 为 AI Agent 深度设计的端到端音视频管线"
    bbox_sub = f_sub.getbbox(sub)
    draw.text(((WIDTH - (bbox_sub[2] - bbox_sub[0])) // 2, 650), sub, font=f_sub, fill=COLORS['text_sub'])

    img.save(output_path)
    return output_path

def build_scene2(output_path):
    """场景2: 命令行 CLI 实战与核心使用方法"""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_title = get_font(32)
    f_desc = get_font(18)
    f_mono = get_font(15)
    f_badge = get_font(14)
    f_card_t = get_font(20)
    f_card_d = get_font(15)

    draw_capsule(draw, (80, 50, 110, 30), "使用方法", f_badge, COLORS['accent_green'], (20, 45, 30, 255), COLORS['accent_green'])
    draw.text((205, 48), "命令行 CLI 实战与快捷指令调用", font=f_title, fill=COLORS['text_main'])
    draw.text((80, 92), "无需物理显卡与图形界面，一行命令极速触发云端旁白合成与 1080P 视频渲染", font=f_desc, fill=COLORS['text_sub'])

    # 左侧：CLI 终端模拟
    panel_left = [80, 130, 80 + 960, 130 + 870]
    draw.rounded_rectangle(panel_left, radius=10, fill=COLORS['panel'], outline=COLORS['panel_border'], width=1)
    draw.rectangle([80, 130, 80 + 960, 130 + 38], fill=(18, 20, 24, 255))
    draw.line([80, 130 + 38, 80 + 960, 130 + 38], fill=COLORS['panel_border'], width=1)
    
    draw.ellipse([95, 144, 107, 156], fill=(255, 95, 87, 255))
    draw.ellipse([115, 144, 127, 156], fill=(254, 188, 46, 255))
    draw.ellipse([135, 144, 147, 156], fill=(40, 200, 64, 255))
    draw.text((160, 140), "bash: ~/opencut-video-generator", font=f_badge, fill=COLORS['text_muted'])

    cli_lines = [
        ("# 1. 安装核心音视频依赖", COLORS['text_muted']),
        ("$ pip install -r requirements.txt", COLORS['accent_cyan']),
        ("[INFO] 成功安装 edge-tts>=6.1.9, Pillow>=10.0.0, requests", COLORS['accent_green']),
        ("", COLORS['text_main']),
        ("# 2. 默认模式一键合成演示视频", COLORS['text_muted']),
        ("$ python3 generate.py", COLORS['accent_cyan']),
        (">>> [1/4] 合成云端旁白语音 (Edge-TTS zh-CN-YunxiNeural)...", COLORS['text_sub']),
        (">>> [2/4] 渲染多场景高保真 1080P 分镜 (Pillow / 25FPS)...", COLORS['text_sub']),
        (">>> [3/4] 调度 FFmpeg 复合滤镜图合成多轨道视频...", COLORS['text_sub']),
        ("🎉 视频生成完成！输出路径: output/opencut_tutorial.mp4", COLORS['accent_green']),
        ("", COLORS['text_main']),
        ("# 3. 高级命令行参数说明", COLORS['text_muted']),
        ("$ python3 generate.py \\", COLORS['accent_cyan']),
        ("    --text \"大家好，这是自定义的一键生成技术视频！\" \\", COLORS['accent_blue']),
        ("    --output \"output/custom_demo.mp4\" \\", COLORS['accent_purple']),
        ("    --temp-dir \"temp_build\"", COLORS['accent_amber'])
    ]
    cy = 185
    for line, color in cli_lines:
        draw.text((105, cy), line, font=f_mono, fill=color)
        cy += 45

    # 右侧：CLI 参数详解卡片
    cards = [
        ("参数一: --text", "旁白脚本文本", "支持任意长文本输入，自动调用 Edge-TTS 高效合成自然专业神经语音", COLORS['accent_blue']),
        ("参数二: --output", "导出 MP4 路径", "指定最终合成的 1080P/25FPS H.264+AAC 视频文件路径", COLORS['accent_purple']),
        ("参数三: --temp-dir", "临时切片缓存", "隔离保存对齐音频、分镜 PNG 图片及临时 FFmpeg 图层", COLORS['accent_green'])
    ]

    rx = 1070
    ry = 130
    rw = 770
    rh = 265
    for title, badge, desc, col in cards:
        draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=10, fill=COLORS['panel'], outline=COLORS['card_border'], width=1)
        draw.text((rx + 30, ry + 25), title, font=f_card_t, fill=COLORS['text_main'])
        draw_capsule(draw, (rx + rw - 150, ry + 25, 120, 28), badge, f_badge, col, (20, 30, 45, 255), col)
        draw.line([rx + 30, ry + 70, rx + rw - 30, ry + 70], fill=COLORS['card_border'], width=1)
        draw.text((rx + 30, ry + 95), desc, font=f_card_d, fill=COLORS['text_sub'])
        ry += rh + 38

    img.save(output_path)
    return output_path

def build_scene3(output_path):
    """场景3: 实景多轨道时间轴与 AI 操控"""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_title = get_font(30)
    f_desc = get_font(18)
    f_mono = get_font(14)
    f_badge = get_font(14)
    f_ui = get_font(13)

    draw_capsule(draw, (80, 50, 140, 30), "剪辑器引擎", f_badge, COLORS['accent_purple'], (35, 25, 55, 255), COLORS['accent_purple'])
    draw.text((235, 48), "模块化多轨道时间轴与 AI 自动化操控", font=f_title, fill=COLORS['text_main'])
    draw.text((80, 92), "通过标准 Web/桌面端渲染底座，AI Agent 可通过 MCP 协议毫秒级操作轨道与切片", font=f_desc, fill=COLORS['text_sub'])

    # 左侧：AI Agent 终端
    panel_left = [80, 130, 80 + 820, 130 + 440]
    draw.rounded_rectangle(panel_left, radius=10, fill=COLORS['panel'], outline=COLORS['panel_border'], width=1)
    draw.rectangle([80, 130, 80 + 820, 130 + 38], fill=(18, 20, 24, 255))
    draw.line([80, 130 + 38, 80 + 820, 130 + 38], fill=COLORS['panel_border'], width=1)
    
    draw.ellipse([95, 144, 107, 156], fill=(255, 95, 87, 255))
    draw.ellipse([115, 144, 127, 156], fill=(254, 188, 46, 255))
    draw.ellipse([135, 144, 147, 156], fill=(40, 200, 64, 255))
    draw.text((160, 140), "agent-terminal: ~/opencut-mcp-executor", font=f_ui, fill=COLORS['text_muted'])

    code_lines = [
        ("> opencut-agent --action=auto-compose --input=article.md", COLORS['accent_cyan']),
        ("[1/4] 解析文案分镜结构与语音权重... 耗时: 120ms", COLORS['text_sub']),
        ("[2/4] 调用 edge-tts 生成对齐旁白音轨 (zh-CN-YunxiNeural)", COLORS['accent_green']),
        ("[3/4] 触发 OpenCut 剪辑器 API: POST /api/timeline/import", COLORS['accent_blue']),
        ("      -> 导入视频切片: scene_intro.mp4 (00:00:00 - 00:00:30)", COLORS['text_sub']),
        ("      -> 导入波形音轨: narration.mp3 (振幅对齐完成)", COLORS['text_sub']),
        ("      -> 动态插入逐字字幕层 (对齐精度: 10ms)", COLORS['text_sub']),
        ("[4/4] 剪辑工程已就绪，正在实时预览渲染...", COLORS['accent_amber'])
    ]
    cy = 185
    for line, color in code_lines:
        draw.text((105, cy), line, font=f_mono, fill=color)
        cy += 38

    # 右侧：视频监视窗口
    panel_right = [930, 130, 930 + 910, 130 + 440]
    draw.rounded_rectangle(panel_right, radius=10, fill=(10, 11, 14, 255), outline=COLORS['panel_border'], width=1)
    draw.rounded_rectangle([945, 145, 945 + 880, 145 + 410], radius=8, fill=(18, 20, 25, 255), outline=(32, 36, 44, 255), width=1)
    
    draw_capsule(draw, (965, 165, 80, 26), "● REC", f_badge, COLORS['accent_red'], (40, 15, 15, 255), (100, 30, 30, 255))
    draw.text((1060, 168), "CAM-1: 1920x1080 @ 60FPS", font=f_ui, fill=COLORS['text_muted'])
    draw.text((945 + 880 - 130, 168), "00:00:14.28", font=f_ui, fill=COLORS['accent_cyan'])
    
    draw.ellipse([945 + 440 - 35, 145 + 205 - 35, 945 + 440 + 35, 145 + 205 + 35], fill=(30, 35, 45, 200), outline=COLORS['accent_blue'], width=2)
    draw.polygon([(945 + 440 - 10, 145 + 205 - 18), (945 + 440 - 10, 145 + 205 + 18), (945 + 440 + 18, 145 + 205)], fill=COLORS['text_main'])

    # 底部：多轨道时间轴面板
    tl = [80, 595, 80 + 1760, 595 + 420]
    draw.rounded_rectangle(tl, radius=10, fill=COLORS['panel'], outline=COLORS['panel_border'], width=1)
    
    # 时间轴控制工具栏
    draw.rectangle([80, 595, 80 + 1760, 595 + 42], fill=(18, 20, 24, 255))
    draw.line([80, 595 + 42, 80 + 1760, 595 + 42], fill=COLORS['panel_border'], width=1)
    draw.text((105, 606), "时间轴编排区 (Timeline Tracks)", font=f_badge, fill=COLORS['text_main'])
    draw.text((360, 606), "00:00:00", font=f_ui, fill=COLORS['text_muted'])
    draw.text((800, 606), "00:00:10", font=f_ui, fill=COLORS['text_muted'])
    draw.text((1240, 606), "00:00:20", font=f_ui, fill=COLORS['text_muted'])
    draw.text((1680, 606), "00:00:30", font=f_ui, fill=COLORS['text_muted'])

    tracks = [
        ("视频轨 (Video 1)", 650, (35, 30, 55, 255), (80, 65, 130, 255), "clip_intro_4k.mp4 [00:00:00 - 00:00:30]", COLORS['accent_purple']),
        ("音频轨 (Audio 1)", 760, (20, 35, 30, 255), (40, 90, 65, 255), "narration_yunxi_ai.mp3", COLORS['accent_green']),
        ("字幕轨 (Subtitle)", 870, (25, 35, 50, 255), (50, 80, 130, 255), "AI 逐字对齐字幕流 (自动断句与换行)", COLORS['accent_cyan'])
    ]

    for label, ty, bg_col, border_col, tag_text, tag_col in tracks:
        draw.rounded_rectangle([100, ty, 250, ty + 90], radius=6, fill=(16, 18, 22, 255), outline=COLORS['card_border'], width=1)
        draw.text((115, ty + 35), label, font=f_badge, fill=COLORS['text_main'])
        
        track_box = [265, ty, 1815, ty + 90]
        draw.rounded_rectangle(track_box, radius=6, fill=bg_col, outline=border_col, width=1)
        draw_capsule(draw, (280, ty + 12, 14, 14), "", f_badge, tag_col, tag_col)
        draw.text((305, ty + 10), tag_text, font=f_ui, fill=COLORS['text_main'])
        
        if "Audio" in label:
            draw_waveform(draw, 280, ty + 35, 1500, 45, (63, 185, 80, 180))

    img.save(output_path)
    return output_path

def build_scene4(output_path):
    """场景4: 技术架构与三大核心支柱"""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_title = get_font(34)
    f_sub = get_font(20)
    f_card_t = get_font(24)
    f_card_d = get_font(16)
    f_badge = get_font(14)

    draw_capsule(draw, (80, 60, 140, 34), "技术架构支柱", f_badge, COLORS['accent_blue'], (20, 35, 60, 255), COLORS['accent_blue'])
    draw.text((235, 58), "构建现代自动化音视频流水线", font=f_title, fill=COLORS['text_main'])
    draw.text((80, 110), "三大核心架构支柱，兼具极速本地性能与无缝多平台云端扩展能力", font=f_sub, fill=COLORS['text_sub'])

    cards = [
        {
            "num": "01",
            "title": "全无头 CI/CD 自动化",
            "badge": "无头流水线",
            "b_col": COLORS['accent_blue'],
            "b_bg": (20, 35, 60, 255),
            "points": [
                "· 无需物理显卡与真实显示器",
                "· Linux CPU 环境 FFmpeg 极速渲染",
                "· GitHub Actions 秒级云端批量构建"
            ]
        },
        {
            "num": "02",
            "title": "毫秒级语音与多轨合成",
            "badge": "神经语音",
            "b_col": COLORS['accent_green'],
            "b_bg": (20, 45, 30, 255),
            "points": [
                "· 接入 Edge-TTS 自然专业神经声线",
                "· FFmpeg 复合滤镜图多轨合成引擎",
                "· 动态播放红针与音频波形毫秒卡点"
            ]
        },
        {
            "num": "03",
            "title": "纯正开源与零豆腐块",
            "badge": "100% 开源",
            "b_col": COLORS['accent_purple'],
            "b_bg": (35, 25, 55, 255),
            "points": [
                "· MIT 协议开放，绝无商用版权隐患",
                "· 挂载文泉驿中文字体杜绝豆腐块",
                "· 配合 .gitignore 保持 Git 极致轻量"
            ]
        }
    ]

    card_w = 560
    card_h = 760
    card_y = 190
    spacing = 40
    start_x = 80

    for i, c in enumerate(cards):
        cx = start_x + i * (card_w + spacing)
        box = [cx, card_y, cx + card_w, card_y + card_h]
        draw.rounded_rectangle(box, radius=12, fill=COLORS['panel'], outline=COLORS['card_border'], width=1)
        
        # 头部编号条
        draw_capsule(draw, (cx + 35, card_y + 35, 55, 30), c['num'], f_badge, c['b_col'], c['b_bg'], c['b_col'])
        draw_capsule(draw, (cx + 105, card_y + 35, 120, 30), c['badge'], f_badge, c['b_col'], c['b_bg'])

        # 标题
        draw.text((cx + 35, card_y + 90), c['title'], font=f_card_t, fill=COLORS['text_main'])
        draw.line([cx + 35, card_y + 135, cx + card_w - 35, card_y + 135], fill=COLORS['card_border'], width=1)

        # 核心点
        py = card_y + 160
        for pt in c['points']:
            draw.text((cx + 35, py), pt, font=f_card_d, fill=COLORS['text_sub'])
            py += 45

    img.save(output_path)
    return output_path
