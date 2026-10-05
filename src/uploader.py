import subprocess
import json

def upload_to_uguu(video_path):
    """
    将生成的 MP4 视频文件上传至 Uguu (https://uguu.se) 临时文件托管平台以获取公网预览链接
    """
    cmd = [
        'curl', '-s',
        '-F', f'files[]=@{video_path}',
        'https://uguu.se/upload.php'
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        if data.get('success') and data.get('files'):
            url = data['files'][0]['url']
            print(f"🌐 视频已成功上传至公网临时托管！")
            print(f"🔗 在线预览链接: {url}")
            return url
        else:
            print("⚠️ 上传至 Uguu 失败:", res.stdout)
            return None
    except Exception as e:
        print("❌ 上传过程发生异常:", str(e))
        return None
