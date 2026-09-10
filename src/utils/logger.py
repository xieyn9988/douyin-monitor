# src/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 确保日志目录存在
Path("logs").mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    获取一个配置好的日志记录器
    用法：logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    # 1. 文件日志（按大小轮转，每个 10MB，保留 5 个备份）
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10*1024*1024, 
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(file_handler)
    
    # 2. 控制台日志（输出到终端，方便实时查看）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    ))
    logger.addHandler(console_handler)
    
    return logger