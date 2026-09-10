# src/processor/audio.py
import subprocess
import os
from pathlib import Path

class AudioProcessor:
    def __init__(self, output_dir: str = "./audio_cache"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def extract_audio(self, video_url: str, video_id: str) -> str:
        """使用yt-dlp下载视频并用FFmpeg提取音频"""
        output_path = self.output_dir / f"{video_id}.mp3"
        
        # 使用yt-dlp获取视频流
        cmd_download = [
            'yt-dlp', '-f', 'bestaudio', 
            '--extract-audio', '--audio-format', 'mp3',
            '--audio-quality', '0',
            '-o', str(output_path),
            video_url
        ]
        
        # 添加重试逻辑
        for retry in range(3):
            try:
                subprocess.run(cmd_download, check=True, timeout=120)
                return str(output_path)
            except subprocess.TimeoutExpired:
                continue
        raise Exception(f"Failed to extract audio for {video_id}")
    
    def get_audio_features(self, audio_path: str) -> dict:
        """使用ffprobe获取音频元数据"""
        cmd = [
            'ffprobe', '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams',
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        import json
        data = json.loads(result.stdout)
        return {
            'duration': float(data['format']['duration']),
            'bitrate': int(data['format']['bit_rate']),
            'sample_rate': data['streams'][0]['sample_rate']
        }