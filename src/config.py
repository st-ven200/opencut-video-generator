import os

# 基础分辨率与帧率
WIDTH = 1920
HEIGHT = 1080
FPS = 25

# 字体配置 (文泉驿微米黑 / 兼容中英文抗锯齿)
FONT_FILE = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'

# Stripe / Linear 高级暗色调色板
COLORS = {
    'bg': (13, 14, 17, 255),          # #0d0e11 顶级深黑石墨
    'panel': (22, 24, 29, 255),       # #16181d 窗口与面板底色
    'panel_border': (40, 44, 52, 255),# #282c34 极细边框
    'card_bg': (18, 20, 24, 255),     # #121418 卡片背景
    'card_border': (36, 40, 48, 255), # #242830 卡片微边框
    'text_main': (240, 243, 246, 255),# #f0f3f6 主标题高亮
    'text_sub': (154, 163, 178, 255), # #9aa3b2 副标题及正文
    'text_muted': (100, 110, 125, 255),# 弱化提示
    'accent_blue': (56, 139, 253, 255),# #388bfd 强调蓝
    'accent_green': (63, 185, 80, 255),# #3fb950 强调绿
    'accent_red': (248, 81, 73, 255),  # #f85149 时间轴播放红指针
    'accent_purple': (163, 113, 247, 255), # #a371f7 紫色标签
    'accent_cyan': (56, 189, 248, 255),    # #38bdf8 终端高亮青
    'accent_amber': (217, 119, 6, 255)     # #d97706 暖琥珀
}

# 默认分镜场景时长 (秒)
SCENE_TIMINGS = {
    'scene1_end': 6.5,
    'scene2_end': 20.0,
    'scene3_end': 29.7
}
