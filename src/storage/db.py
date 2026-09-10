# src/storage/db.py
import sqlite3
from pathlib import Path
from datetime import datetime
from .models import Video, TaskLog

class Database:
    def __init__(self, db_path="data/videos.db"):
        self.db_path = db_path
        Path("data").mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 视频表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                title TEXT,
                url TEXT,
                cover_url TEXT,
                audio_path TEXT,
                duration REAL,
                created_at TIMESTAMP,
                processed INTEGER DEFAULT 0
            )
        ''')
        
        # 任务日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                status TEXT,
                error_msg TEXT,
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_video(self, video):
        """插入或更新视频"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO videos 
            (id, user_id, title, url, cover_url, audio_path, duration, created_at, processed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            video.id, 
            video.user_id, 
            video.title, 
            video.url, 
            video.cover_url,
            video.audio_path, 
            video.duration, 
            video.created_at.isoformat() if video.created_at else None, 
            1 if video.processed else 0
        ))
        conn.commit()
        conn.close()
    
    def get_video(self, video_id):
        """根据ID查询视频"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Video(
                id=row['id'],
                user_id=row['user_id'],
                title=row['title'],
                url=row['url'],
                cover_url=row['cover_url'],
                audio_path=row['audio_path'],
                duration=row['duration'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                processed=bool(row['processed'])
            )
        return None
    
    def get_all_videos(self, limit=20):
        """获取所有视频（用于调试）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def log_task(self, task_name, status, error_msg=None, retry_count=0):
        """记录任务日志"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO task_logs (task_name, status, error_msg, retry_count)
            VALUES (?, ?, ?, ?)
        ''', (task_name, status, error_msg, retry_count))
        conn.commit()
        conn.close()