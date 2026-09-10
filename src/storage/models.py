# src/storage/models.py
from datetime import datetime

class Video:
    """视频数据模型 - 纯 Python 类，对应数据库表"""
    def __init__(self, id=None, user_id=None, title=None, url=None, 
                 cover_url=None, audio_path=None, duration=None, 
                 created_at=None, processed=False):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.url = url
        self.cover_url = cover_url
        self.audio_path = audio_path
        self.duration = duration
        self.created_at = created_at or datetime.now()
        self.processed = processed
    
    def to_dict(self):
        """转为字典，方便调试"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'url': self.url,
            'cover_url': self.cover_url,
            'audio_path': self.audio_path,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed': self.processed
        }
    
    def __repr__(self):
        return f"<Video(id={self.id}, title={self.title[:20]}...)>"


class TaskLog:
    """任务日志模型"""
    def __init__(self, id=None, task_name=None, status=None, 
                 error_msg=None, retry_count=0, created_at=None):
        self.id = id
        self.task_name = task_name
        self.status = status
        self.error_msg = error_msg
        self.retry_count = retry_count
        self.created_at = created_at or datetime.now()