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
    """场景1: 开篇 Hook - Kafka 为什么这么快"""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_huge = get_font(64)
    f_sub = get_font(26)
    f_badge = get_font(18)

    draw_capsule(draw, (WIDTH // 2 - 190, 440, 380, 44), "100% 开源 · B站硬核架构解密", f_badge, COLORS['accent_blue'], (20, 35, 60, 255), COLORS['accent_blue'])
    
    title = "Kafka 为什么这么快？"
    bbox = f_huge.getbbox(title)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, 510), title, font=f_huge, fill=COLORS['text_main'])

    sub = "百万级吞吐量的终极奥秘：零拷贝原理 (mmap/sendfile) 与 RocketMQ 架构抉择"
    bbox_sub = f_sub.getbbox(sub)
    draw.text(((WIDTH - (bbox_sub[2] - bbox_sub[0])) // 2, 620), sub, font=f_sub, fill=COLORS['text_sub'])

    img.save(output_path)
    return output_path

def build_scene2(output_path):
    """场景2: 传统 I/O 痛点 (4次上下文切换 + 4次内存拷贝)"""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_title = get_font(32)
    f_desc = get_font(18)
    f_badge = get_font(14)
    f_card_t = get_font(20)
    f_mono = get_font(15)

    draw_capsule(draw, (80, 50, 160, 30), "传统 I/O 瓶颈", f_badge, COLORS['accent_red'], (40, 15, 15, 255), COLORS['accent_red'])
    draw.text((255, 48), "传统数据传输路径 (4次上下文切换 + 4次内存拷贝)", font=f_title, fill=COLORS['text_main'])
    draw.text((80, 92), "数据必须在内核态与用户态之间来回复制，极其消耗 CPU 资源与内存带宽", font=f_desc, fill=COLORS['text_sub'])

    # 上区域：用户态内存 (User Space)
    user_space = [80, 130, 80 + 1760, 130 + 330]
    draw.rounded_rectangle(user_space, radius=10, fill=COLORS['panel'], outline=COLORS['panel_border'], width=1)
    draw.text((110, 150), "用户态空间 (User Space Application Memory)", font=f_card_t, fill=COLORS['text_main'])
    draw_capsule(draw, (1500, 150, 150, 28), "应用进程内存", f_badge, COLORS['accent_blue'], (20, 35, 60, 255))
    
    app_buf = [580, 220, 580 + 760, 220 + 180]
    draw.rounded_rectangle(app_buf, radius=8, fill=(25, 35, 55, 255), outline=COLORS['accent_blue'], width=1)
    draw.text((610, 240), "用户态应用程序缓冲区 (User Application Buffer)", font=f_mono, fill=COLORS['text_main'])
    draw.text((610, 290), "② 从内核读缓冲区拷贝到应用内存  |  ③ 从应用内存拷贝到 Socket 缓冲区", font=f_mono, fill=COLORS['text_sub'])

    # 下区域：内核态空间 (Kernel Space)
    kernel_space = [80, 500, 80 + 1760, 500 + 510]
    draw.rounded_rectangle(kernel_space, radius=10, fill=(15, 20, 25, 255), outline=COLORS['card_border'], width=1)
    draw.text((110, 520), "内核态空间与物理硬件 (Kernel Space & Hardware)", font=f_card_t, fill=COLORS['text_main'])

    # 磁盘 vs 内核 Read Buffer vs Socket Buffer vs 网卡
    box_disk = [110, 580, 110 + 360, 580 + 380]
    draw.rounded_rectangle(box_disk, radius=8, fill=(25, 20, 20, 255), outline=COLORS['card_border'], width=1)
    draw.text((130, 600), "磁盘物理存储 (Disk)", font=f_card_t, fill=COLORS['accent_red'])
    draw.text((130, 650), "① DMA 拷贝", font=f_mono, fill=COLORS['text_sub'])

    box_read = [530, 580, 530 + 420, 580 + 380]
    draw.rounded_rectangle(box_read, radius=8, fill=(20, 35, 30, 255), outline=COLORS['accent_green'], width=1)
    draw.text((550, 600), "内核读缓冲区 (Read Buffer)", font=f_card_t, fill=COLORS['accent_green'])
    draw.text((550, 650), "PageCache 页面缓存", font=f_mono, fill=COLORS['text_sub'])

    box_socket = [1000, 580, 1000 + 420, 580 + 380]
    draw.rounded_rectangle(box_socket, radius=8, fill=(30, 25, 40, 255), outline=COLORS['accent_purple'], width=1)
    draw.text((1020, 600), "Socket 发送缓冲区", font=f_card_t, fill=COLORS['accent_purple'])
    draw.text((1020, 650), "TCP 发送队列", font=f_mono, fill=COLORS['text_sub'])

    box_nic = [1470, 580, 1470 + 340, 580 + 380]
    draw.rounded_rectangle(box_nic, radius=8, fill=(20, 35, 50, 255), outline=COLORS['accent_cyan'], width=1)
    draw.text((1490, 600), "物理网卡 (NIC)", font=f_card_t, fill=COLORS['accent_cyan'])
    draw.text((1490, 650), "④ DMA 发送网络", font=f_mono, fill=COLORS['text_sub'])

    img.save(output_path)
    return output_path

def build_scene3(output_path):
    """场景3: 零拷贝原理 (mmap 内存映射 vs sendfile 物理直传)"""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_title = get_font(32)
    f_desc = get_font(18)
    f_badge = get_font(14)
    f_card_t = get_font(22)
    f_card_d = get_font(16)
    f_mono = get_font(15)

    draw_capsule(draw, (80, 50, 140, 30), "零拷贝原理", f_badge, COLORS['accent_blue'], (20, 35, 60, 255), COLORS['accent_blue'])
    draw.text((235, 48), "mmap 内存映射 vs sendfile DMA 物理直传网络卡", font=f_title, fill=COLORS['text_main'])
    draw.text((80, 92), "通过 sendfile 系统调用与 DMA 散射聚集，彻底实现 CPU 零内存拷贝与 2 次上下文切换", font=f_desc, fill=COLORS['text_sub'])

    # 左面板：mmap (内存映射)
    mmap_box = [80, 140, 80 + 860, 140 + 870]
    draw.rounded_rectangle(mmap_box, radius=10, fill=COLORS['panel'], outline=COLORS['panel_border'], width=1)
    draw.text((110, 165), "方案一：mmap 内存映射 (Memory Mapping)", font=f_card_t, fill=COLORS['text_main'])
    draw_capsule(draw, (720, 165, 180, 28), "3次拷贝 + 4次切换", f_badge, COLORS['accent_amber'], (40, 30, 15, 255))
    draw.line([110, 210, 910, 210], fill=COLORS['card_border'], width=1)

    mmap_points = [
        ("· 虚拟内存映射", "用户态虚拟内存直接指向内核缓冲区地址", COLORS['accent_blue']),
        ("· 省去 1 次 CPU 拷贝", "数据不需要从内核态复制到用户态应用内存", COLORS['accent_green']),
        ("· 适用场景", "适合需要对数据进行小幅度修改或随机读写的场景", COLORS['text_sub'])
    ]
    my = 230
    for t_sub, desc_sub, col_sub in mmap_points:
        draw.text((110, my), t_sub, font=f_mono, fill=col_sub)
        draw.text((110, my + 30), desc_sub, font=f_card_d, fill=COLORS['text_sub'])
        my += 80

    # mmap 架构示意
    draw.rounded_rectangle([110, 500, 910, 970], radius=8, fill=(18, 22, 28, 255), outline=COLORS['card_border'], width=1)
    draw.text((130, 520), "[磁盘] --> (DMA) --> [内核读缓冲区] ==== (虚拟内存映射) ====> [用户应用]", font=f_mono, fill=COLORS['accent_cyan'])
    draw.text((130, 570), "                             || (CPU 拷贝)", font=f_mono, fill=COLORS['text_muted'])
    draw.text((130, 620), "                             \\/ ", font=f_mono, fill=COLORS['text_muted'])
    draw.text((130, 670), "                     [Socket 发送缓冲区] --> (DMA) --> [网卡]", font=f_mono, fill=COLORS['accent_purple'])

    # 右面板：sendfile (DMA 散射聚集物理直传)
    sf_box = [980, 140, 980 + 860, 140 + 870]
    draw.rounded_rectangle(sf_box, radius=10, fill=(15, 22, 20, 255), outline=COLORS['accent_green'], width=1)
    draw.text((1010, 165), "方案二：sendfile 系统调用 (真正的零拷贝)", font=f_card_t, fill=COLORS['accent_green'])
    draw_capsule(draw, (1610, 165, 200, 28), "0次 CPU 拷贝 + 2次切换", f_badge, COLORS['accent_green'], (20, 45, 30, 255))
    draw.line([1010, 210, 1810, 210], fill=COLORS['card_border'], width=1)

    sf_points = [
        ("· Linux 2.4+ 内核优化", "使用 DMA Scatter-Gather 描述符句柄直传", COLORS['accent_green']),
        ("· CPU 零内存拷贝", "数据直接从内核缓冲区传输至网卡，CPU 不参与搬运", COLORS['accent_cyan']),
        ("· 极速网络吞吐", "上下文切换减少 50%，极致释放 CPU 算力与内存带宽", COLORS['accent_purple'])
    ]
    sy = 230
    for t_sub, desc_sub, col_sub in sf_points:
        draw.text((1010, sy), t_sub, font=f_mono, fill=col_sub)
        draw.text((1010, sy + 30), desc_sub, font=f_card_d, fill=COLORS['text_sub'])
        sy += 80

    # sendfile 架构示意
    draw.rounded_rectangle([1010, 500, 1810, 970], radius=8, fill=(12, 28, 22, 255), outline=COLORS['accent_green'], width=1)
    draw.text((1030, 540), "[磁盘 File]", font=f_card_t, fill=COLORS['accent_red'])
    draw.text((1030, 600), "   || (DMA 拷贝)", font=f_mono, fill=COLORS['text_muted'])
    draw.text((1030, 650), "   \\/ ", font=f_mono, fill=COLORS['text_muted'])
    draw.text((1030, 700), "[内核 PageCache 读缓冲区]", font=f_card_t, fill=COLORS['accent_green'])
    draw.text((1030, 760), "   || (DMA 直传网卡, CPU 0 参与数据搬运！)", font=f_mono, fill=COLORS['accent_cyan'])
    draw.text((1030, 810), "   \\/ ", font=f_mono, fill=COLORS['text_muted'])
    draw.text((1030, 860), "[物理网卡 NIC]", font=f_card_t, fill=COLORS['accent_purple'])

    img.save(output_path)
    return output_path

def build_scene4(output_path):
    """场景4: Kafka 4 大极速底座卡片」"""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_title = get_font(34)
    f_sub = get_font(20)
    f_card_t = get_font(24)
    f_card_d = get_font(16)
    f_badge = get_font(14)

    draw_capsule(draw, (80, 60, 160, 34), "Kafka 极速内核", f_badge, COLORS['accent_purple'], (35, 25, 55, 255), COLORS['accent_purple'])
    draw.text((255, 58), "Kafka 轻松跑出 200 万级吞吐量的四大技术底座", font=f_title, fill=COLORS['text_main'])
    draw.text((80, 110), "零拷贝 + PageCache + 顺序写磁盘 + 批量压缩，构建现代高性能消息引擎", font=f_sub, fill=COLORS['text_sub'])

    cards = [
        {
            "num": "01",
            "title": "sendfile 零拷贝",
            "badge": "0 次 CPU 拷贝",
            "b_col": COLORS['accent_blue'],
            "b_bg": (20, 35, 60, 255),
            "points": [
                "· 数据从磁盘内核缓冲区直传网卡",
                "· 上下文切换减少 50%",
                "· 内存带宽利用率提升 300%"
            ]
        },
        {
            "num": "02",
            "title": "Linux PageCache",
            "badge": "物理内存缓存",
            "b_col": COLORS['accent_green'],
            "b_bg": (20, 45, 30, 255),
            "points": [
                "· 充分利用 Linux 闲置物理内存缓存数据",
                "· 绝大多数读写直接命中内存",
                "· 避开 JVM GC 开销与大堆内存停顿"
            ]
        },
        {
            "num": "03",
            "title": "顺序写 (Sequential I/O)",
            "badge": "磁盘追加模式",
            "b_col": COLORS['accent_purple'],
            "b_bg": (35, 25, 55, 255),
            "points": [
                "· 日志文件仅支持追加写入 (Append-only)",
                "· 彻底消除机械硬盘随机磁头寻道",
                "· 顺序写磁盘速度堪比内存写入"
            ]
        },
        {
            "num": "04",
            "title": "批量合并与压缩",
            "badge": "高效压缩",
            "b_col": COLORS['accent_amber'],
            "b_bg": (40, 30, 15, 255),
            "points": [
                "· Producer 端批量打包合并消息",
                "· 支持 Zstd / Snappy / Gzip 算法",
                "· 大幅缩减网络 I/O 传输开销"
            ]
        }
    ]

    card_w = 410
    card_h = 760
    card_y = 190
    spacing = 40
    start_x = 80

    for i, c in enumerate(cards):
        cx = start_x + i * (card_w + spacing)
        box = [cx, card_y, cx + card_w, card_y + card_h]
        draw.rounded_rectangle(box, radius=12, fill=COLORS['panel'], outline=COLORS['card_border'], width=1)
        
        draw_capsule(draw, (cx + 30, card_y + 30, 50, 28), c['num'], f_badge, c['b_col'], c['b_bg'], c['b_col'])
        draw_capsule(draw, (cx + 90, card_y + 30, 130, 28), c['badge'], f_badge, c['b_col'], c['b_bg'])

        draw.text((cx + 30, card_y + 85), c['title'], font=f_card_t, fill=COLORS['text_main'])
        draw.line([cx + 30, card_y + 130, cx + card_w - 30, card_y + 130], fill=COLORS['card_border'], width=1)

        py = card_y + 155
        for pt in c['points']:
            draw.text((cx + 25, py), pt, font=f_card_d, fill=COLORS['text_sub'])
            py += 45

    img.save(output_path)
    return output_path

def build_scene5(output_path):
    """场景5: Kafka vs RocketMQ 选型对比表格"""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    f_title = get_font(34)
    f_sub = get_font(20)
    f_card_t = get_font(24)
    f_card_d = get_font(16)
    f_badge = get_font(14)
    f_mono = get_font(15)

    draw_capsule(draw, (80, 60, 160, 34), "架构选型对比", f_badge, COLORS['accent_amber'], (40, 30, 15, 255), COLORS['accent_amber'])
    draw.text((255, 58), "Apache Kafka vs Apache RocketMQ 核心对比与选型指南", font=f_title, fill=COLORS['text_main'])
    draw.text((80, 110), "依据业务场景选择最匹配的消息存储与高并发处理引擎", font=f_sub, fill=COLORS['text_sub'])

    # 左侧：Kafka
    box_kafka = [80, 180, 80 + 860, 180 + 780]
    draw.rounded_rectangle(box_kafka, radius=12, fill=COLORS['panel'], outline=COLORS['accent_purple'], width=1)
    draw_capsule(draw, (110, 210, 80, 32), "Kafka", f_badge, COLORS['accent_purple'], (35, 25, 55, 255), COLORS['accent_purple'])
    draw.text((210, 212), "极致吞吐流处理王者", font=f_card_t, fill=COLORS['text_main'])
    draw.line([110, 260, 910, 260], fill=COLORS['card_border'], width=1)

    kafka_rows = [
        "· 存储架构：每个 Partition 独立物理文件",
        "· 适用场景：海量数据日志收集、实时流计算 (Flink/Spark)",
        "· 吞吐表现：百万级/秒吞吐量，读写全程零拷贝",
        "· 瓶颈防范：Topic/Partition 上千时，文件数过多导致随机写"
    ]
    ky = 290
    for r in kafka_rows:
        draw.text((110, ky), r, font=f_card_d, fill=COLORS['text_sub'])
        ky += 55

    # 右侧：RocketMQ
    box_rmq = [980, 180, 980 + 860, 180 + 780]
    draw.rounded_rectangle(box_rmq, radius=12, fill=(15, 28, 22, 255), outline=COLORS['accent_green'], width=1)
    draw_capsule(draw, (1010, 210, 110, 32), "RocketMQ", f_badge, COLORS['accent_green'], (20, 45, 30, 255), COLORS['accent_green'])
    draw.text((1140, 212), "金融级业务交易与多 Topic 王者", font=f_card_t, fill=COLORS['text_main'])
    draw.line([1010, 260, 1810, 260], fill=COLORS['card_border'], width=1)

    rmq_rows = [
        "· 存储架构：所有 Topic 消息混存入单个 CommitLog 文件",
        "· 适用场景：核心业务交易、电商订单、分布式事务",
        "· 特色功能：支持金融级事务消息、延迟队列与死信队列",
        "· 高并发能力：天然支持上万级 Topic 高并发稳定写入"
    ]
    ry = 290
    for r in rmq_rows:
        draw.text((1010, ry), r, font=f_card_d, fill=COLORS['text_sub'])
        ry += 55

    img.save(output_path)
    return output_path
