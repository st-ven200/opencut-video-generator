import subprocess
import os
from .audio_effects import generate_sfx_pop, generate_sfx_whoosh, generate_sfx_ding, generate_bgm_ambient

def get_audio_duration(audio_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        audio_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 32.0

def render_final_video(scene1_png, logo_png, scene2_png, scene3_png, scene4_png, scene5_png, audio_mp3, output_mp4):
    os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)
    temp_dir = os.path.dirname(os.path.abspath(audio_mp3))
    
    total_dur = get_audio_duration(audio_mp3)
    print(f"Detected narration audio duration: {total_dur:.2f} seconds")

    # 动态生成 SFX 音效与 BGM 背景音乐
    print(">>> 正在生成高保真 SFX 转场音效与科技 Ambient BGM 背景音乐...")
    bgm_path = generate_bgm_ambient(os.path.join(temp_dir, "bgm_tech.wav"), duration=int(total_dur) + 10)
    whoosh_path = generate_sfx_whoosh(os.path.join(temp_dir, "sfx_whoosh.wav"))
    pop_path = generate_sfx_pop(os.path.join(temp_dir, "sfx_pop.wav"))

    # 动态分配 5 个场景的时长占比 (Intro: 10%, 传统I/O: 30%, 零拷贝mmap/sendfile: 30%, 4大底座: 18%, 选型对比: 12%)
    t1 = round(total_dur * 0.10, 2)
    t2 = round(total_dur * 0.40, 2)
    t3 = round(total_dur * 0.70, 2)
    t4 = round(total_dur * 0.88, 2)
    t5 = round(total_dur, 2)

    t1_ms = int(t1 * 1000)
    t2_ms = int(t2 * 1000)
    t3_ms = int(t3 * 1000)
    t4_ms = int(t4 * 1000)

    filter_complex = (
        f"[0:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v0];"
        f"[1:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v1];"
        f"[v0][v1]overlay=(W-w)/2:250[v_scene1];"
        f"[2:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v_scene2];"
        f"[3:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v_scene3];"
        f"[4:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v_scene4];"
        f"[5:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v_scene5];"
        f"[v_scene1]trim=start=0:end={t1},setpts=PTS-STARTPTS[part1];"
        f"[v_scene2]trim=start={t1}:end={t2},setpts=PTS-STARTPTS[part2];"
        f"[v_scene3]trim=start={t2}:end={t3},setpts=PTS-STARTPTS[part3];"
        f"[v_scene4]trim=start={t3}:end={t4},setpts=PTS-STARTPTS[part4];"
        f"[v_scene5]trim=start={t4}:end={t5},setpts=PTS-STARTPTS[part5];"
        f"[part1][part2][part3][part4][part5]concat=n=5:v=1:a=0[v_concat];"
        f"[v_concat]format=yuv420p[v_out];"
        f"[6:a]volume=1.0[a_voice];"
        f"[7:a]volume=0.10,atrim=start=0:end={t5}[a_bgm];"
        f"[8:a]adelay={t1_ms}|{t1_ms},volume=0.7[sfx1];"
        f"[8:a]adelay={t2_ms}|{t2_ms},volume=0.7[sfx2];"
        f"[9:a]adelay={t3_ms}|{t3_ms},volume=0.7[sfx3];"
        f"[9:a]adelay={t4_ms}|{t4_ms},volume=0.7[sfx4];"
        f"[a_voice][a_bgm][sfx1][sfx2][sfx3][sfx4]amix=inputs=6:duration=first:dropout_transition=2[a_out]"
    )

    cmd = [
        'ffmpeg', '-y',
        '-loop', '1', '-i', scene1_png,
        '-loop', '1', '-i', logo_png,
        '-loop', '1', '-i', scene2_png,
        '-loop', '1', '-i', scene3_png,
        '-loop', '1', '-i', scene4_png,
        '-loop', '1', '-i', scene5_png,
        '-i', audio_mp3,
        '-i', bgm_path,
        '-i', whoosh_path,
        '-i', pop_path,
        '-filter_complex', filter_complex,
        '-map', '[v_out]',
        '-map', '[a_out]',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '22',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-r', '25',
        output_mp4
    ]

    print("Running FFmpeg rendering command with 5 detailed scenes, BGM and SFX...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg stderr:", res.stderr)
        raise RuntimeError("FFmpeg rendering failed")
    
    print(f"Video rendering successfully completed -> {output_mp4}")
    return output_mp4
