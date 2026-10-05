import subprocess
import os

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

def render_final_video(scene1_png, logo_png, scene2_png, scene3_png, scene4_png, audio_mp3, output_mp4):
    os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)
    
    total_dur = get_audio_duration(audio_mp3)
    print(f"Detected narration audio duration: {total_dur:.2f} seconds")

    # 动态分配 4 个场景的时长占比 (Intro: 15%, CLI 使用方法: 35%, 剪辑器多轨: 30%, 总结: 20%)
    t1 = round(total_dur * 0.15, 2)
    t2 = round(total_dur * 0.50, 2)
    t3 = round(total_dur * 0.80, 2)
    t4 = round(total_dur, 2)

    filter_complex = (
        f"[0:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v0];"
        f"[1:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v1];"
        f"[v0][v1]overlay=(W-w)/2:280[v_scene1];"
        f"[2:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v_scene2];"
        f"[3:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v3];"
        f"[v3]drawbox=x='265+(w-370)*(t-{t2})/({t3-t2})':y=650:w=4:h=310:color=#f85149@1.0:t=fill[v_scene3];"
        f"[4:v]loop=loop=-1:size=2:start=0,setpts=PTS-STARTPTS[v_scene4];"
        f"[v_scene1]trim=start=0:end={t1},setpts=PTS-STARTPTS[part1];"
        f"[v_scene2]trim=start={t1}:end={t2},setpts=PTS-STARTPTS[part2];"
        f"[v_scene3]trim=start={t2}:end={t3},setpts=PTS-STARTPTS[part3];"
        f"[v_scene4]trim=start={t3}:end={t4},setpts=PTS-STARTPTS[part4];"
        f"[part1][part2][part3][part4]concat=n=4:v=1:a=0[v_concat];"
        f"[v_concat]format=yuv420p[v_out]"
    )

    cmd = [
        'ffmpeg', '-y',
        '-loop', '1', '-i', scene1_png,
        '-loop', '1', '-i', logo_png,
        '-loop', '1', '-i', scene2_png,
        '-loop', '1', '-i', scene3_png,
        '-loop', '1', '-i', scene4_png,
        '-i', audio_mp3,
        '-filter_complex', filter_complex,
        '-map', '[v_out]',
        '-map', '5:a',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '22',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-r', '25',
        output_mp4
    ]

    print("Running FFmpeg rendering command...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg stderr:", res.stderr)
        raise RuntimeError("FFmpeg rendering failed")
    
    print(f"Video rendering successfully completed -> {output_mp4}")
    return output_mp4
